from tinydb import TinyDB, Query
from tinydb.table import Table
import os


class OrderDB:
    def __init__(self, path, limit):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):
            self.db = TinyDB(path)
            self.db.table("order")
        else:
            self.db = TinyDB(path)
        self.limit = limit
        self.path = path

    def insert(self, key, role, content):
        table = self.db.table("order")
        table.insert({"key": key, "role": role, "content": content})

    def query(self, key):
        table = self.db.table("order")
        query = Query()
        results = table.search(query.key == key)
        return results[-self.limit :]




