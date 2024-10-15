import sqlite3
from .models import Member, Blacklist, ServerLog

class DatabaseHandler:
    def __init__(self, db_path='database/bot_database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        self.connect()
        self.cursor.execute(Member.create_table_query())
        self.cursor.execute(Blacklist.create_table_query())
        self.cursor.execute(ServerLog.create_table_query())
        self.conn.commit()
        self.disconnect()

    def add_member(self, member_id, username, joined_at):
        self.connect()
        query = "INSERT INTO members (member_id, username, joined_at) VALUES (?, ?, ?)"
        self.cursor.execute(query, (member_id, username, joined_at))
        self.conn.commit()
        self.disconnect()

    def remove_member(self, member_id):
        self.connect()
        query = "DELETE FROM members WHERE member_id = ?"
        self.cursor.execute(query, (member_id,))
        self.conn.commit()
        self.disconnect()

    def add_to_blacklist(self, member_id, reason, added_by):
        self.connect()
        query = "INSERT INTO blacklist (member_id, reason, added_by) VALUES (?, ?, ?)"
        self.cursor.execute(query, (member_id, reason, added_by))
        self.conn.commit()
        self.disconnect()

    def remove_from_blacklist(self, member_id):
        self.connect()
        query = "DELETE FROM blacklist WHERE member_id = ?"
        self.cursor.execute(query, (member_id,))
        self.conn.commit()
        self.disconnect()

    def is_blacklisted(self, member_id):
        self.connect()
        query = "SELECT * FROM blacklist WHERE member_id = ?"
        self.cursor.execute(query, (member_id,))
        result = self.cursor.fetchone()
        self.disconnect()
        return bool(result)

    def add_server_log(self, event_type, member_id, details):
        self.connect()
        query = "INSERT INTO server_logs (event_type, member_id, details) VALUES (?, ?, ?)"
        self.cursor.execute(query, (event_type, member_id, details))
        self.conn.commit()
        self.disconnect()

    def get_member_info(self, member_id):
        self.connect()
        query = "SELECT * FROM members WHERE member_id = ?"
        self.cursor.execute(query, (member_id,))
        result = self.cursor.fetchone()
        self.disconnect()
        return result

    def update_member_nickname(self, member_id, new_nickname):
        self.connect()
        query = "UPDATE members SET nickname = ? WHERE member_id = ?"
        self.cursor.execute(query, (new_nickname, member_id))
        self.conn.commit()
        self.disconnect()