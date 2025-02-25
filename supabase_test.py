from supabase import create_client, Client
from dotenv import load_dotenv
import os
load_dotenv()

# 初始化Supabase客户端
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# 创建新表的 SQL 查询
create_table_query = """
CREATE TABLE IF NOT EXISTS new_table (
    id BIGSERIAL PRIMARY KEY,
    name TEXT,
    age INTEGER,
    email TEXT UNIQUE
);
"""

try:
    # 执行 SQL 查询以创建表
    response = supabase.sql(create_table_query).execute()

    # 检查响应
    if response.data is not None:
        print("表 'new_table' 已成功创建")
    else:
        print("创建表时出错:", response.error)

except Exception as e:
    print(f"发生异常: {str(e)}")