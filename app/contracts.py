# Author: Eve Murphy
# Student ID: 20049423
# Date: 18/07/2024
# Description: This script contains classes to simulate blockchain node
#              interaction via methods representative of smart contract execution.
#              Classes for proposal, log, and vote are included.

from db import get_db_connection
import datetime

# ProposalContract class for handling proposal-related operations
class ProposalContract:
    @staticmethod
    def vote(proposal_id, vote_type):
        """
        Cast a vote on a proposal.

        Args:
            proposal_id (int): The ID of the proposal to vote on.
            vote_type (str): The type of vote ('yes' or 'no').

        Raises:
            ValueError: If the vote_type is neither 'yes' nor 'no'.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update the proposal vote count based on the vote_type
        if vote_type == 'yes':
            cursor.execute("UPDATE proposal SET proposal_yes_votes = proposal_yes_votes + 1 WHERE proposal_id = %s", (proposal_id,))
        elif vote_type == 'no':
            cursor.execute("UPDATE proposal SET proposal_no_votes = proposal_no_votes + 1 WHERE proposal_id = %s", (proposal_id,))
        else:
            raise ValueError("vote_type must be 'yes' or 'no'")

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def finalize(proposal_id):
        """
        Close a proposal for voting.

        Args:
            proposal_id (int): The ID of the proposal to finalize.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update the proposal status to 'Closed'
        cursor.execute("UPDATE proposal SET proposal_status = 'Closed' WHERE proposal_id = %s", (proposal_id,))
        conn.commit()
        cursor.close()
        conn.close()

# LogContract class for handling log-related operations
class LogContract:
    @staticmethod
    def insert_log(log_title, log_body, log_notes, log_type, org_id):
        """
        Insert a new log entry.

        Args:
            log_title (str): The title of the log entry.
            log_body (str): The body content of the log entry.
            log_notes (str): Additional notes for the log entry.
            log_type (str): The type of log entry (e.g., 'proposal', 'vote').
            org_id (int): The organization ID associated with the log entry.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query to insert a new log entry
        sql = """
            INSERT INTO log (log_title, log_body, log_notes, log_type, org_id, log_timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        timestamp = datetime.datetime.now()
        
        cursor.execute(sql, (log_title, log_body, log_notes, log_type, org_id, timestamp))
        conn.commit()
        cursor.close()
        conn.close()

# VoteContract class for handling vote-related operations
class VoteContract:
    @staticmethod
    def cast_vote(vote_type, proposal_id, member_id):
        """
        Cast a vote on a proposal by a specific member.

        Args:
            vote_type (str): The type of vote ('yes' or 'no').
            proposal_id (int): The ID of the proposal to vote on.
            member_id (int): The ID of the member casting the vote.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query to insert a new vote
        cursor.execute("""
            INSERT INTO vote (vote_value, proposal_id, member_id)
            VALUES (%s, %s, %s)
        """, (vote_type, proposal_id, member_id))
        
        conn.commit()
        cursor.close()
        conn.close()