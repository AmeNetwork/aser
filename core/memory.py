from core.storage.tinydb import TinyDBMemory
from core.storage.supabase import SupabaseMemory
from core.storage.sqlite import SQLiteMemory
from dotenv import load_dotenv
import os
load_dotenv()


class Memory:
    def __init__(self, **db):
        limit = db.get("limit", 5)
        if db["type"] == "tinydb":
            path = db.get("memory", "./cache/database/tiny_db.json")
            self.db = TinyDBMemory(path=path, limit=limit)
        elif db["type"] == "supabase":
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            self.db = SupabaseMemory(supabase_url,supabase_key,db["table"],limit)
        elif db["type"] == "sqlite":
            path = db.get("memory", "./cache/database/sqlite_db.sqlite")
            self.db = SQLiteMemory(path=path, limit=limit)
        else:
            pass

    def insert(self, key, role, content):
        self.db.insert(key, role, content)

    def query(self, key):
        return self.db.query(key)

    def clear(self, key):
        self.db.clear(key)
