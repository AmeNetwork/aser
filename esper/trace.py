import sqlite3
import tiktoken
import os
class Trace:
    def __init__(self,path="./data/database/trace.db",session=None):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.session = session
        self._create_tables()

    def _create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT,
                session TEXT,
                agent_name TEXT,
                agent_model TEXT,
                input TEXT,
                input_token_size INTEGER,
                output TEXT,
                output_token_size INTEGER,
                tools_log TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                feed_back TEXT,
                error TEXT
            )
        """)
        self.conn.commit()

    def set_session(self, session):
        self.session = session

    def count_tokens(self, text, model="gpt-3.5-turbo"):

        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return len(encoding.encode(text))

    def add(
        self,
        uid,
        session,
        agent_name,
        agent_model,
        input,
        output,
        tools_log,
        start_time,
        end_time,
        feed_back,
        error
    ):

        input_token_size = self.count_tokens(input, agent_model)
        output_token_size = self.count_tokens(output, agent_model)

        self.cursor.execute("""
            INSERT INTO traces (uid, session, agent_name, agent_model, input, input_token_size,
                                output, output_token_size, tools_log, start_time, end_time,
                                feed_back, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (uid, session, agent_name, agent_model, input, input_token_size, output,
              output_token_size, tools_log, start_time, end_time, feed_back, error))
        self.conn.commit()


    def __del__(self):
        self.conn.close()