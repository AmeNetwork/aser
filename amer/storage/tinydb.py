from tinydb import TinyDB, Query
from tinydb.table import Table
import os


class TinyDBMemory:
    def __init__(self, path, limit):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):
            self.db = TinyDB(path)
            self.db.table("memory")
        else:
            self.db = TinyDB(path)
        self.limit = limit
        self.path = path

    def insert(self, key, role, content):
        table = self.db.table("memory")
        table.insert({"key": key, "role": role, "content": content})

    def query(self, key):
        table = self.db.table("memory")
        query = Query()
        results = table.search(query.key == key)
        return results[-self.limit :]

    def clear(self, key):
        table = self.db.table("memory")
        query = Query()
        table.remove(query.key == key)


