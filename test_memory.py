from core.storage.supabase import SupabaseMemory
from core.storage.sqlite import SQLiteMemory
from dotenv import load_dotenv
import os
load_dotenv()
# supabase_url = os.getenv("SUPABASE_URL")
# supabase_key = os.getenv("SUPABASE_KEY")

# supbase=SupabaseMemory(supabase_url,supabase_key,"agent_memory",2)

# supbase.insert("test","user2","hello world2")

# print(supbase.query("test"))
# supbase.clear("test")

# def test(name="jack",age=10):
#     print(name)
#     print(age)

# test()


sqlLiteMemory=SQLiteMemory("./cache/database/sqlite_db.sqlite",2)

sqlLiteMemory.insert("test","user2","hello world2")

result=sqlLiteMemory.query("test")
sqlLiteMemory.clear("test")
result=sqlLiteMemory.query("test")
print(result)
