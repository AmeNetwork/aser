import duckdb
from datetime import datetime

class Trace:
    def __init__(self):
        self.conn = duckdb.connect('trace.db')
        self._create_tables()

    def _create_tables(self):

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                uid VARCHAR(50),
                session VARCHAR(50) UNIQUE,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                id INTEGER PRIMARY KEY,
                session VARCHAR(50),
                agent_name VARCHAR(50),
                agent_model VARCHAR(50),
                input TEXT,
                input_token_size INTEGER,
                output TEXT,
                output_token_size INTEGER,
                tools_log TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                feed_back TEXT,
                error TEXT,
                FOREIGN KEY (session) REFERENCES sessions(session)
            )
        """)

    def create_trace_session(self, uid):
        session = f"{uid}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        current_time = datetime.now()
        
        self.conn.execute("""
            INSERT OR REPLACE INTO sessions (uid, session, created_at, updated_at)
            VALUES (?, ?, 
                    COALESCE((SELECT created_at FROM sessions WHERE uid = ?), ?),
                    ?)
        """, [uid, session, uid, current_time, current_time])
        
        return session


    def add_trace(
        self,
        session,
        agent_name,
        agent_model,
        input,
        input_token_size,
        output,
        output_token_size,
        tools_log,
        start_time,
        end_time,
        feed_back,
        error
    ):
        self.conn.execute("""
            INSERT INTO traces (session, agent_name, agent_model, input, input_token_size,
                                output, output_token_size, tools_log, start_time, end_time,
                                feed_back, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [session, agent_name, agent_model, input, input_token_size, output,
              output_token_size, tools_log, start_time, end_time, feed_back, error])



    def clear_trace_session(self):
        self.conn.execute("DELETE FROM traces")
        self.conn.execute("DELETE FROM sessions")

    def get_trace_session(self, uid):
        result = self.conn.execute("""
            SELECT session, created_at, updated_at
            FROM sessions
            WHERE uid = ?
            ORDER BY updated_at DESC
            LIMIT 1
        """, [uid])
        return result.fetchone()

    def get_trace_by_session(self, session):
        result = self.conn.execute("SELECT * FROM traces WHERE session = ?", [session])
        return result.fetchall()

    def __del__(self):
        self.conn.close()