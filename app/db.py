# Author: Eve Murphy
# Student ID: 20049423
# Date: 18/07/2024
# Description: This script contains database functionalities necessary for creating
#              & inserting new entries. Session & database connection handling is also included.

import mysql.connector
import hashlib

# Helper function to hash passwords
def hash_password(password):
    """
    Hash a plaintext password using SHA-256.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """
    Establish a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
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

# Session handling

def login(email, password):
    """
    Authenticate a user by email and password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: A dictionary containing the user's information if authentication is successful.
              None if authentication fails.
    """
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
    """
    Retrieve a proposal by its ID.

    Args:
        proposal_id (int): The ID of the proposal.

    Returns:
        dict: A dictionary containing the proposal details.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch proposal details
    query = "SELECT * FROM proposal WHERE proposal_id = %s"
    cursor.execute(query, (proposal_id,))
    proposal = cursor.fetchone()

    cursor.close()
    conn.close()

    return proposal

def insert_proposal(proposal_title, proposal_body, member_id):
    """
    Insert a new proposal into the database.

    Args:
        proposal_title (str): The title of the proposal.
        proposal_body (str): The body content of the proposal.
        member_id (int): The ID of the member creating the proposal.
    """
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
    """
    Retrieve general community proposals not associated with the user's team.

    Args:
        team_id (int): The ID of the user's team.

    Returns:
        list: A list of dictionaries containing general proposal details.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
    """
    Retrieve proposals associated with the user's team.

    Args:
        team_id (int): The ID of the user's team.

    Returns:
        list: A list of dictionaries containing team proposal details.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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

    return team_proposals

# Thread

def get_comments_by_proposal_id(proposal_id):
    """
    Retrieve comments for a specific proposal.

    Args:
        proposal_id (int): The ID of the proposal.

    Returns:
        list: A list of dictionaries containing comment details.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch comments for a specific proposal
    query = """
    SELECT c.thread_content, c.thread_timestamp, c.member_id
    FROM thread c 
    WHERE c.proposal_id = %s
    ORDER BY c.thread_timestamp ASC
    """
    cursor.execute(query, (proposal_id,))
    results = cursor.fetchall()
    
    if results:
        # Fetch member information separately
        member_ids = [result['member_id'] for result in results]
        member_info = get_members_info(cursor, member_ids)
        
        # Map member info to results
        for result in results:
            member_id = result['member_id']
            result['member_firstname'] = member_info[member_id]['member_firstname']
            result['member_lastname'] = member_info[member_id]['member_lastname']

    cursor.close()
    conn.close()
    
    return results

def insert_comment(proposal_id, member_id, thread_content, thread_timestamp):
    """
    Insert a new comment into the database.

    Args:
        proposal_id (int): The ID of the proposal being commented on.
        member_id (int): The ID of the member making the comment.
        thread_content (str): The content of the comment.
        thread_timestamp (datetime): The timestamp of the comment.

    Returns:
        int: The ID of the newly inserted comment.
    """
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
    """
    Retrieve the first name and last name of a member by their ID.

    Args:
        member_id (int): The ID of the member.

    Returns:
        tuple: A tuple containing the first name and last name of the member.
               If the member is not found, (None, None) is returned.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch member name by ID
    cursor.execute("SELECT member_firstname, member_lastname FROM member WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        fname = result['member_firstname']
        lname = result['member_lastname']
        return fname, lname
    else:
        return None, None  # Or handle the case appropriately

def get_member_information(member_id):
    """
    Retrieve detailed information of a member by their ID.

    Args:
        member_id (int): The ID of the member.

    Returns:
        dict: A dictionary containing the member's information.
    """
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

def get_members_info(cursor, member_ids):
    """
    Retrieve information of multiple members by their IDs.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor.
        member_ids (list): A list of member IDs.

    Returns:
        dict: A dictionary mapping member IDs to their respective information.
    """
    # Query to fetch member information for given member_ids
    query = """
    SELECT member_id, member_firstname, member_lastname
    FROM member
    WHERE member_id IN ({})
    """.format(','.join(['%s'] * len(member_ids)))
    
    cursor.execute(query, member_ids)
    member_info = {row['member_id']: row for row in cursor.fetchall()}
    
    return member_info

def get_member_proposals(member_id):
    """
    Retrieve proposals created by a specific member.

    Args:
        member_id (int): The ID of the member.

    Returns:
        list: A list of dictionaries containing the member's proposals.
    """
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

    return member_proposals

def get_member_votes(member_id):
    """
    Retrieve votes cast by a specific member.

    Args:
        member_id (int): The ID of the member.

    Returns:
        list: A list of dictionaries containing the member's votes and proposal titles.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch member votes along with proposal titles
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

def has_user_voted(member_id, proposal_id):
    """
    Check if a user has voted on a specific proposal.

    Args:
        member_id (int): The ID of the member.
        proposal_id (int): The ID of the proposal.

    Returns:
        bool: True if the user has voted on the proposal, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vote WHERE proposal_id = %s AND member_id = %s", (proposal_id, member_id))
    has_voted = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return has_voted

# Log

def get_log_entries():
    """
    Retrieve all log entries from the database.

    Returns:
        list: A list of dictionaries containing log entries.
    """
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
    """
    Retrieve team information associated with a specific member.

    Args:
        member_id (int): The ID of the member.

    Returns:
        dict: A tuple containing the team ID and team name.
    """
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
    cursor.close()
    conn.close()

    return team_info[0]