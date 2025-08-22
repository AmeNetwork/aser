import chromadb
from aser.utils import get_chunks, get_file_data



class Knowledge:
    def __init__(self, name, path="./data/knowledge", query_ns=5):
        self.chroma_client = chromadb.PersistentClient(path)
        self.collection = self.chroma_client.get_or_create_collection(name)
        self.query_ns = query_ns

    def upsert(self, ids, documents, metadatas=None):
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    def delete(self, id):
        self.collection.delete(ids=[id])

    def query(self, query_texts, query_ns=None, where=None, where_document=None):
        results = self.collection.query(
            query_texts=query_texts,
            n_results=query_ns or self.query_ns,
            where=where,
            where_document=where_document,
        )
        return results

    def destory(self):
        self.chroma_client.delete_collection(self.collection.name)

    def knowledger_from_file(self, file_path, chunk_size=300):
        file_data = get_file_data(file_path)
        chunks = get_chunks(file_data, chunk_size)
        ids = [str(i) for i in range(len(chunks))]
        self.upsert(ids, documents=chunks)


