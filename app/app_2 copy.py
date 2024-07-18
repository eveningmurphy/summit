from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db_connection
from contracts import ProposalContract
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'orangemountain' # Ensure to use a secure key in production

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Routes

@app.route('/')
def index():
    if 'member_id' in session:
        member_id = session['member_id']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch user's team ID and name
        cursor.execute("""
            SELECT m.team_id, t.team_name
            FROM member m
            LEFT JOIN team t ON m.team_id = t.team_id
            WHERE m.member_id = %s
        """, (member_id,))
        team_info = cursor.fetchone()
        
        if team_info:
            team_id = team_info['team_id']
            team_name = team_info['team_name']
        else:
            team_id = None
            team_name = "Unknown"  # Default name if no team found
        
        # Fetch proposals from user's team including team name
        cursor.execute("""
            SELECT p.*, t.team_name AS team_name
            FROM proposal p
            JOIN member m ON p.member_id = m.member_id
            LEFT JOIN team t ON m.team_id = t.team_id
            WHERE m.team_id = %s
        """, (team_id,))
        team_proposals = cursor.fetchall()
        
        # Fetch general proposals (not from the user's team) including team name
        cursor.execute("""
            SELECT p.*, t.team_name AS team_name
            FROM proposal p
            LEFT JOIN member m ON p.member_id = m.member_id
            LEFT JOIN team t ON m.team_id = t.team_id
            WHERE m.team_id != %s OR m.team_id IS NULL
        """, (team_id,))
        general_proposals = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('index.html', team_proposals=team_proposals, general_proposals=general_proposals, team_name=team_name, route="home")
    else:
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'member_id' in session:
        return render_template('dashboard.html', route="dashboard")
    else:
        return redirect(url_for('login'))

@app.route('/log')
def log():
    if 'member_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all log entries chronologically
        cursor.execute("""
            SELECT *
            FROM log
            ORDER BY log_timestamp DESC
        """)
        logs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('log.html', logs=logs, route="log")
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM member WHERE member_email = %s AND member_password = %s", (email, password))
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        if member:
            session['member_id'] = member['member_id']
            session['member_name'] = f"{member['member_firstname']} {member['member_lastname']}"
            
            # Insert a log entry for login
            log_title = f"Member Login"
            log_body = f"Member {session['member_name']} logged into the system."
            log_notes = ""
            org_id = 1  # Replace with your organization's ID
            
            contracts.LogContract.insert_log(log_title, log_body, log_notes, org_id)
            
            return redirect(url_for('index'))
        else:
            return "Login failed. Please check your credentials and try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('member_id', None)
    session.pop('member_name', None)
    
    # Insert a log entry for logout
    log_title = f"Member Logout"
    log_body = f"Member {session.get('member_name', 'Unknown')} logged out from the system."
    log_notes = ""
    org_id = 1  # Replace with your organization's ID
    
    LogContract.insert_log(log_title, log_body, log_notes, org_id)
    
    return redirect(url_for('login'))

@app.route('/proposal/<int:proposal_id>', methods=['GET'])
def proposal(proposal_id):
    if 'member_id' not in session:
        return redirect(url_for('login'))
    
    proposal = get_proposal_by_id(proposal_id)  # Function to fetch proposal details from the DB
    comments = get_comments_by_proposal_id(proposal_id)  # Function to fetch comments from the DB
    has_voted = has_user_voted(session['member_id'], proposal_id)
    
    return render_template('proposal.html', proposal=proposal, comments=comments, has_voted=has_voted)

@app.route('/add_comment/<int:proposal_id>', methods=['POST'])
def add_comment(proposal_id):
    if 'member_id' not in session:
        return jsonify({'success': False}), 403
    
    member_id = session['member_id']
    thread_content = request.form['thread_content']
    thread_timestamp = datetime.datetime.now()
    
    # Insert comment into the database
    new_comment_id = insert_comment(proposal_id, member_id, thread_content, thread_timestamp)
    
    if new_comment_id:
        member_name = get_member_name_by_id(member_id)  # Function to fetch member name from the DB
        comment = {
            'thread_content': thread_content,
            'thread_timestamp': thread_timestamp,
            'member_name': member_name,
        }
        return jsonify({'success': True, 'comment': comment})
    else:
        return jsonify({'success': False})

@app.route('/submit_proposal', methods=['GET', 'POST'])
def submit_proposal():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        member_id = session['member_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proposal (proposal_title, proposal_body, proposal_priority, proposal_majority, proposal_status, proposal_timestamp, proposal_yes_votes, proposal_no_votes, member_id)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)
            """, (title, body, 'Normal', 50, 'Open', 0, 0, member_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Insert a log entry for proposal submission
        log_title = f"Proposal Created by Member {member_id}"
        log_body = f"A new proposal titled '{title}' has been submitted."
        log_notes = ""
        org_id = 1  # Replace with your organization's ID
        
        LogContract.insert_log(log_title, log_body, log_notes, org_id)
        
        return redirect(url_for('index'))
    
    return render_template('submit_proposal.html')

@app.route('/vote', methods=['POST'])
def vote():
    proposal_id = request.form['proposal_id']
    vote_type = request.form['vote_type']
    member_id = session['member_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vote (vote_value, proposal_id, member_id)
        VALUES (%s, %s, %s)
    """, (vote_type, proposal_id, member_id))
    conn.commit()
    
    ProposalContract.vote(proposal_id, vote_type)
    
    # Insert a log entry for voting
    log_title = f"Vote Submitted by Member {member_id}"
    log_body = f"Member {member_id} voted {vote_type} on proposal {proposal_id}."
    log_notes = ""
    org_id = 1  # Replace with your organization's ID
    
    LogContract.insert_log(log_title, log_body, log_notes, org_id)
    
    return redirect(url_for('proposal', id=proposal_id))

@app.route('/finalize/<int:id>')
def finalize(id):
    ProposalContract.finalize(id)
    return redirect(url_for('proposal', id=id))

if __name__ == '__main__':
    app.run(debug=True)