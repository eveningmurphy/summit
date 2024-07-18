import mysql.connector
import hashlib

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    # Add your database configuration
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="summit"
    )
    
    """ old config
        conn = mysql.connector.connect(
        host="localhost",
        user="summit", # root
        password="summ1t!*", # root
        database="summit"
    )
    """
    return conn

# Functionalities for app.py

# Session handling

def login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Encrypt & test hash in deployment for security

    cursor.execute("SELECT * FROM member WHERE member_email = %s AND member_password = %s", (email, password))
    member = cursor.fetchone()

    cursor.close()
    conn.close()

    return member

# Proposal

def get_proposal_by_id(proposal_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch proposal details
    query = "SELECT * FROM proposal WHERE proposal_id = %s"
    cursor.execute(query, (proposal_id,))
    return cursor.fetchone()

def get_comments_by_proposal_id(proposal_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch comments for a specific proposal
    query = """
    SELECT c.thread_content, c.thread_timestamp, m.member_firstname, m.member_lastname 
    FROM thread c 
    JOIN member m ON c.member_id = m.member_id 
    WHERE c.proposal_id = %s
    ORDER BY c.thread_timestamp ASC
    """
    cursor.execute(query, (proposal_id,))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

def insert_proposal(proposal_title, proposal_body, member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO proposal (proposal_title, proposal_body, proposal_priority, proposal_majority, proposal_status, proposal_timestamp, proposal_yes_votes, proposal_no_votes, member_id)
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)
        """, (proposal_title, proposal_body, 'Normal', 50, 'Open', 0, 0, member_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_general_proposals(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()

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

    return general_proposals

def get_team_proposals(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch proposals from user's team including team name
    cursor.execute("""
        SELECT p.*, t.team_name AS team_name
        FROM proposal p
        JOIN member m ON p.member_id = m.member_id
        LEFT JOIN team t ON m.team_id = t.team_id
        WHERE m.team_id = %s
    """, (team_id,))

    team_proposals = cursor.fetchall()
    cursor.close()
    conn.close()

    return team_proposals[0]

# Thread

def insert_comment(proposal_id, member_id, thread_content, thread_timestamp):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to insert a new comment
    query = """
    INSERT INTO thread (proposal_id, member_id, thread_content, thread_timestamp) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (proposal_id, member_id, thread_content, thread_timestamp))
    conn.commit()  # Commit the transaction to the database
    
    # Retrieve the last inserted ID
    cursor.execute("SELECT LAST_INSERT_ID() AS thread_id")
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result['thread_id']

# User/member

def get_member_name_by_id(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch member name by ID
    cursor.execute("SELECT member_firstname, member_lastname FROM member WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()  # Use fetchone instead of fetchAll

    cursor.close()
    conn.close()

    if result:
        fname = result['member_firstname']
        lname = result['member_lastname']
        return fname, lname
    else:
        return None, None  # Or handle the case appropriately

def get_member_information(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch member's information (fullname, email, role, level)
    cursor.execute("""
        SELECT member_firstname, member_lastname, member_email, member_role, member_level
        FROM member
        WHERE member_id = %s
    """, (member_id,))

    member_info = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return member_info

def get_member_proposals(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch member proposals
    cursor.execute("""
    SELECT proposal_id, proposal_title
    FROM proposal
    WHERE member_id = %s
    """, (member_id,))
    
    member_proposals = cursor.fetchall()
    cursor.close()
    conn.close()

    return member_proposals[0]

def get_member_votes(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT v.*, p.proposal_title
    FROM vote v
    JOIN proposal p ON v.proposal_id = p.proposal_id
    WHERE v.member_id = %s
    """, (member_id,))

    member_votes = cursor.fetchall()
    cursor.close()
    conn.close()

    return member_votes

# Return true/false for if a user has voted on a specific proposal
def has_user_voted(member_id, proposal_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vote WHERE proposal_id = %s AND member_id = %s", (proposal_id, member_id))
    has_voted = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return has_voted

# Log

def get_log_entries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM log
        ORDER BY log_timestamp DESC
    """)
    logs = cursor.fetchall()

    cursor.close()
    conn.close()
    return logs

# Team

def get_team_info(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetch user's team ID and name
    cursor.execute("""
        SELECT m.team_id, t.team_name
        FROM member m
        LEFT JOIN team t ON m.team_id = t.team_id
        WHERE m.member_id = %s
    """, (member_id,))

    team_info = cursor.fetchall()
    cursor.close()
    conn.close()

    return team_info[0]