from core.storage.supabase import SupabaseMemory
from core.storage.sqlite import SQLiteMemory
from dotenv import load_dotenv
from core.memory import Memory
import os
load_dotenv()


memory=Memory(type="supabase",table="agent_memory",limit=10)


memory.insert(key="jimmy",role="user",content="hello world")
result=memory.query("jimmy")
print(result)





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


# sqlLiteMemory=SQLiteMemory("./cache/database/sqlite_db.sqlite",2)

# sqlLiteMemory.insert("test","user2","hello world2")

# result=sqlLiteMemory.query("test")
# sqlLiteMemory.clear("test")
# result=sqlLiteMemory.query("test")
# print(result)
