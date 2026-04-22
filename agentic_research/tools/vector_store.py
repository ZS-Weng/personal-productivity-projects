from config import CHROMA_DIR
import chromadb

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

def delete_collection(collection_name):
    if collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(collection_name)
def get_collection(collection_name):
    if collection_name in [c.name for c in client.list_collections()]:
        collection = client.get_collection(collection_name)
    else:
        collection = client.create_collection(collection_name)
    return collection

def add_to_collection(collection_name,documents,ids,metadatas):
    collection = get_collection(collection_name)
    collection.add(documents=documents, ids=ids, metadatas=metadatas)

def query_collection(query, collection_name):
    collection = get_collection(collection_name)
    results = collection.query(query_texts=[f"{query}"], n_results=5)
    return results