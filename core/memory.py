from tinydb import TinyDB, Query
from tinydb.table import Table

class Memory :
    def __init__(self,provider,path="./memory/tiny_db.json",limit=20) :
        self.provider=provider
        self.limit=limit
        self.path=path

    def insert(self,**data) :
        if self.provider=="tinydb" :
            db = TinyDB(self.path)
            table = db.table(data["key"])
            table.insert({
                "role": data["role"],
                "content":data["content"]
            })
    
    def get(self,**data) :
        if self.provider=="tinydb" :
            db = TinyDB(self.path)
            table = db.table(data["key"])
            return  table.all()[-self.limit:]

    def clear(self,**data) :
        if self.provider=="tinydb" :
            db = TinyDB(self.path)
            table = db.table(data["key"])
            table.truncate()

