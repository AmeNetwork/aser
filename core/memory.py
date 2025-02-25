from core.storage.tinydb import TinyDBMemory


class Memory:
    def __init__(self, **db):
        if db["type"] == "tinydb":
            self.db = TinyDBMemory(path=db["path"], limit=db["limit"])

    def insert(self, key, role, content):
        self.db.insert(key, role, content)

    def query(self, key):
        return self.db.query(key)

    def clear(self, key):
        self.db.clear(key)
