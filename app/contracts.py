# Author: Eve Murphy
# Student ID: 20049423
# Date: 18/07/2024
# Description: This script contains classes to simulate blockchain ndoe
#              interaction via methods representative of smart contract execution.
#              Classes for proposal, log, and vote are included.

from db import get_db_connection
import datetime

# ProposalContract class for handling log operations
class ProposalContract:
    @staticmethod
    def vote(proposal_id, vote_type):
        conn = get_db_connection()
        cursor = conn.cursor()
        if vote_type == 'yes':
            cursor.execute("UPDATE proposal SET proposal_yes_votes = proposal_yes_votes + 1 WHERE proposal_id = %s", (proposal_id,))
        elif vote_type == 'no':
            cursor.execute("UPDATE proposal SET proposal_no_votes = proposal_no_votes + 1 WHERE proposal_id = %s", (proposal_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def finalize(proposal_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE proposal SET proposal_status = 'Closed' WHERE proposal_id = %s", (proposal_id,))
        conn.commit()
        cursor.close()
        conn.close()

# LogContract class for handling log operations
class LogContract:
    @staticmethod
    def insert_log(log_title, log_body, log_notes, log_type, org_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Prepare the SQL query to insert a new log entry
        sql = """
            INSERT INTO log (log_title, log_body, log_notes, log_type, org_id, log_timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        timestamp = datetime.datetime.now()
        cursor.execute(sql, (log_title, log_body, log_notes, log_type, org_id, timestamp))
        conn.commit()
        
        cursor.close()
        conn.close()

# VoteContract class for handling user votes
class VoteContract:
    @staticmethod
    def cast_vote(vote_type, proposal_id, member_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vote (vote_value, proposal_id, member_id)
            VALUES (%s, %s, %s)
        """, (vote_type, proposal_id, member_id))
        conn.commit()
        
        cursor.close()
        conn.close()