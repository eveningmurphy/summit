# Author: Eve Murphy
# Student ID: 20049423
# Date: 18/07/2024
# Description: This script is the main executable for the Summit application.
#              Routes for each page on the web app are included here, with back-end
#              database functionality imported from db.py & contract.py.
#              To start the application, execute this script.

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import datetime
import contracts
import db

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'orangemountain'  # Ensure to use a secure key in production

# Route for the home page
@app.route('/')
def index():
    """
    Render the home page with team and general proposals.
    """
    if 'member_id' in session:
        member_id = session['member_id']
        conn = db.get_db_connection()
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

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page with member information, proposals, and votes.
    """
    if 'member_id' in session:
        member_id = session['member_id']

        # Get all member info
        member_info = db.get_member_information(member_id)
        # Fetch member's proposals
        member_proposals = db.get_member_proposals(member_id)
        # Fetch member's votes
        member_votes = db.get_member_votes(member_id)

        return render_template('dashboard.html', member_info=member_info, member_proposals=member_proposals, member_votes=member_votes, route="dashboard")
    else:
        return redirect(url_for('login'))

# Route for the log page
@app.route('/log')
def log():
    """
    Render the log page with log entries.
    """
    if 'member_id' in session:
        # Fetch all log entries chronologically
        logs = db.get_log_entries()
        return render_template('log.html', logs=logs, route="log")
    else:
        return redirect(url_for('login'))

# Route for the login page and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        member = db.login(email, password)
        if member:
            session['member_id'] = member['member_id']
            session['member_name'] = f"{member['member_firstname']} {member['member_lastname']}"
            
            # Insert a log entry for login
            #log_title = f"Member Login"
            #log_body = f"Member {session['member_name']} logged into the system."
            #log_notes = ""
            #org_id = 1  # Replace with your organization's ID
            
            #LogContract.insert_log(log_title, log_body, log_notes, org_id)
            
            return redirect(url_for('index'))
        else:
            return "Login failed. Please check your credentials and try again."
    return render_template('login.html')

# Route for logging out
@app.route('/logout')
def logout():
    """
    Handle user logout.
    """
    session.pop('member_id', None)
    session.pop('member_name', None)
    
    # Insert a log entry for logout
    #log_title = f"Member Logout"
    #log_body = f"Member {session.get('member_name', 'Unknown')} logged out from the system."
    #log_notes = ""
    #org_id = 1  # Replace with your organization's ID
    
    #LogContract.insert_log(log_title, log_body, log_notes, org_id)
    
    return redirect(url_for('login'))

# Route for viewing a specific proposal
@app.route('/proposal/<int:id>', methods=['GET'])
def proposal(id):
    """
    Display a specific proposal with its comments.
    """
    if 'member_id' not in session:
        return redirect(url_for('login'))
    
    proposal = db.get_proposal_by_id(id)  # Function to fetch proposal details from the DB
    comments = db.get_comments_by_proposal_id(id)  # Function to fetch comments from the DB
    has_voted = db.has_user_voted(session['member_id'], id)
    
    return render_template('proposal.html', proposal=proposal, comments=comments, has_voted=has_voted)

# Route for adding a comment to a proposal
@app.route('/add_comment/<int:proposal_id>', methods=['POST'])
def add_comment(proposal_id):
    """
    Add a comment to a specific proposal.
    """
    if 'member_id' not in session:
        return jsonify({'success': False}), 403
    
    member_id = session['member_id']
    thread_content = request.form['thread_content']
    thread_timestamp = datetime.datetime.now()
    
    # Insert comment into the database
    new_comment_id = db.insert_comment(proposal_id, member_id, thread_content, thread_timestamp)
    
    if new_comment_id:
        member_firstname, member_lastname = db.get_member_name_by_id(member_id)  # Function to fetch member name from the DB
        member_name = member_firstname + " " + member_lastname
        print("membername: ", member_name)
        comment = {
            'thread_content': thread_content,
            'thread_timestamp': thread_timestamp,
            'member_name': member_name
        }
        return jsonify({'success': True, 'comment': comment})
    else:
        return jsonify({'success': False})

# Route for submitting a new proposal
@app.route('/submit_proposal', methods=['GET', 'POST'])
def submit_proposal():
    """
    Handle submission of a new proposal.
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        member_id = session['member_id']
        db.insert_proposal(title, body, member_id)
        
        # Insert a log entry for proposal submission - simulated smart contract class
        log_title = f"Proposal Created by Member {member_id}"
        log_body = f"A new proposal titled '{title}' has been submitted."
        log_notes = ""
        org_id = 1  # Replace with your organization's ID
        
        contracts.LogContract.insert_log(log_title, log_body, log_notes, 'proposal', org_id)
        
        return redirect(url_for('index'))
    
    return render_template('submit_proposal.html')

# Route for voting on a proposal
@app.route('/vote', methods=['POST'])
def vote():
    """
    Handle voting on a proposal.
    """
    proposal_id = request.form['proposal_id']
    vote_type = request.form['vote_type']
    member_id = session['member_id']
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vote (vote_value, proposal_id, member_id)
        VALUES (%s, %s, %s)
    """, (vote_type, proposal_id, member_id))
    conn.commit()
    
    contracts.ProposalContract.vote(proposal_id, vote_type)
    
    # Insert a log entry for voting
    log_title = f"Vote Submitted by Member {member_id}"
    log_body = f"Member {member_id} voted {vote_type} on proposal {proposal_id}."
    log_notes = ""
    org_id = 1  # Replace with your organization's ID
    
    contracts.LogContract.insert_log(log_title, log_body, log_notes, "vote", org_id)
    
    return redirect(url_for('proposal', id=proposal_id))

# Route for finalizing a proposal
@app.route('/finalize/<int:id>')
def finalize(id):
    """
    Finalize a specific proposal.
    """
    contracts.ProposalContract.finalize(id)
    return redirect(url_for('proposal', id=id))

# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)