from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import datetime
import contracts
import db

app = Flask(__name__)
app.secret_key = 'orangemountain' # Ensure to use a secure key in production

# Routes

@app.route('/')
def index():
    if 'member_id' in session:
        member_id = session['member_id']
        
        # Fetch user's team ID and name
        team_info = db.get_team_info(member_id)
        if team_info:
            team_id, team_name = team_info
        else:
            team_id = None
            team_name = "Unknown"  # Default name if no team found

        # Fetch proposals from user's team including team name
        team_proposals = db.get_team_proposals(team_id)
        # Fetch general proposals (not from the user's team) including team name
        general_proposals = db.get_general_proposals(team_id)
        
        return render_template('index.html', team_proposals=team_proposals, general_proposals=general_proposals, team_name=team_name, route="home")
    else:
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
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
    
@app.route('/log')
def log():
    if 'member_id' in session:
        # Fetch all log entries chronologically
        logs = db.get_log_entries()
        return render_template('log.html', logs=logs, route="log")
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/logout')
def logout():
    session.pop('member_id', None)
    session.pop('member_name', None)
    
    # Insert a log entry for logout
    #log_title = f"Member Logout"
    #log_body = f"Member {session.get('member_name', 'Unknown')} logged out from the system."
    #log_notes = ""
    #org_id = 1  # Replace with your organization's ID
    
    #LogContract.insert_log(log_title, log_body, log_notes, org_id)
    
    return redirect(url_for('login'))

@app.route('/proposal/<int:id>', methods=['GET'])
def proposal(id):
    if 'member_id' not in session:
        return redirect(url_for('login'))
    
    proposal = db.get_proposal_by_id(id)  # Function to fetch proposal details from the DB
    comments = db.get_comments_by_proposal_id(id)  # Function to fetch comments from the DB
    has_voted = db.has_user_voted(session['member_id'], id)
    
    return render_template('proposal.html', proposal=proposal, comments=comments, has_voted=has_voted)

@app.route('/add_comment/<int:proposal_id>', methods=['POST'])
def add_comment(proposal_id):
    if 'member_id' not in session:
        return jsonify({'success': False}), 403
    
    member_id = session['member_id']
    thread_content = request.form['thread_content']
    thread_timestamp = datetime.datetime.now()
    
    # Insert comment into the database
    new_comment_id = db.insert_comment(proposal_id, member_id, thread_content, thread_timestamp)
    
    if new_comment_id:
        member_firstname, member_lastname = db.get_member_name_by_id(member_id)  # Function to fetch member name from the DB
        member_name = member_firstname+" "+member_lastname
        print("membername: ",member_name)
        comment = {
            'thread_content': thread_content,
            'thread_timestamp': thread_timestamp,
            'member_name': member_name
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
        db.insert_proposal(title, body, member_id)
        
        # Insert a log entry for proposal submission - simulated smart contract class
        log_title = f"Proposal Created by Member {member_id}"
        log_body = f"A new proposal titled '{title}' has been submitted."
        log_notes = ""
        org_id = 1  # Replace with your organization's ID
        
        contracts.LogContract.insert_log(log_title, log_body, log_notes, 'proposal', org_id)
        
        return redirect(url_for('index'))
    
    return render_template('submit_proposal.html')

@app.route('/vote', methods=['POST'])
def vote():
    # Simulated smart contract operations
    proposal_id = request.form['proposal_id']
    vote_type = request.form['vote_type']
    member_id = session['member_id']
    
    contracts.VoteContract.cast_vote(vote_type, proposal_id, member_id)
    contracts.ProposalContract.vote(proposal_id, vote_type)
    
    # Insert a log entry for voting
    log_title = f"Vote Submitted by Member {member_id}"
    log_body = f"Member {member_id} voted {vote_type} on proposal {proposal_id}."
    log_notes = ""
    org_id = 1  # Replace with your organization's ID
    
    contracts.LogContract.insert_log(log_title, log_body, log_notes, "vote", org_id)
    
    return redirect(url_for('proposal', id=proposal_id))

@app.route('/finalize/<int:id>')
def finalize(id):
    contracts.ProposalContract.finalize(id)
    return redirect(url_for('proposal', id=id))

if __name__ == '__main__':
    app.run(debug=True)