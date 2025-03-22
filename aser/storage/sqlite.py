import sqlite3
import os
import json

class SQLiteMemory:
    def __init__(self, path, limit):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.limit = limit
        self.path = path
        self.conn = sqlite3.connect(path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                key TEXT,
                role TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

    def insert(self, key, role, content):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO memory (key, role, content)
            VALUES (?, ?, ?)
        ''', (key, role, content))
        self.conn.commit()

    def query(self, key):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT role, content FROM memory
            WHERE key = ?
            ORDER BY rowid DESC
            LIMIT ?
        ''', (key, self.limit))
        results = cursor.fetchall()
        return [{"role": role, "content": content} for role, content in reversed(results)]

    def clear(self, key):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM memory WHERE key = ?', (key,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
