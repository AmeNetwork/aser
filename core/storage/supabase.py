from supabase import create_client


class SupabaseMemory:
    def __init__(self, url, key, table_name, limit):

        self.supabase = create_client(url, key)

        self._isExist(table_name)

        self.table_name = table_name

        self.limit = limit

    def _isExist(self, table_name):
        try:
            self.supabase.table(table_name).select("*").limit(1).execute()
        except Exception as e:
            
            
            print(f"There is no {table_name} table in supabase")

    def insert(self, key, role, content):
        self.supabase.table(self.table_name).insert(
            {"key": key, "role": role, "content": content}
        ).execute()

    def query(self, key):
        response = (
            self.supabase.table(self.table_name)
            .select("role", "content")
            .eq("key", key)
            .order("id", desc=True)
            .limit(self.limit)
            .execute()
        )
        return response.data[::-1]

    def clear(self, key):
        self.supabase.table(self.table_name).delete().eq("key", key).execute()
