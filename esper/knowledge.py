import chromadb


class Knowledge:
    def __init__(self, name, path="./data/knowledge", query_ns=5):
        self.chroma_client = chromadb.PersistentClient(path)
        self.collection = self.chroma_client.get_or_create_collection(name)
        self.query_ns = query_ns

    def upsert(self, data):
        documents = []
        metadatas = []
        ids = []
        for item in data:
            documents.append(item["document"])
            metadatas.append(item["metadata"])
            ids.append(item["id"])
        self.collection.upsert(documents=documents, metadatas=metadatas, ids=ids)

    def delete(self, id):
        self.collection.delete(ids=[id])

    def query(self,query_texts, query_ns=None, where=None, where_document=None):
        results = self.collection.query(
            query_texts=query_texts,
            n_results=query_ns or self.query_ns,
            where=where,
            where_document=where_document,
        )
        return results

    def destory(self):
        self.chroma_client.delete_collection(self.collection.name) 

        