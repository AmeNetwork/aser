from tinydb import TinyDB, Query
from tinydb.table import Table
import os
class TinyDBMemory:
    def __init__(self, path="./cache/database/tiny_db.json", limit=20):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.limit = limit
        self.path = path
        self.db=TinyDB(path)
    
    def insert(self, key, role, content):
        table = self.db.table(key)
        table.insert({"role": role, "content": content})
    
    def query(self, key):
        table = self.db.table(key)
        return table.all()[-self.limit:]

    def clear(self, key):
        table = self.db.table(key)
        table.truncate()