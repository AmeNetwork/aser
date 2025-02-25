from core.storage.supabase import SupabaseMemory
from dotenv import load_dotenv
import os
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supbase=SupabaseMemory(supabase_url,supabase_key,"agent_memory",2)

# supbase.insert("test","user2","hello world2")

print(supbase.query("test"))
# supbase.clear("test")

# def test(name="jack",age=10):
#     print(name)
#     print(age)

# test()



