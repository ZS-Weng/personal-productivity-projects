from config import CHROMA_DIR
import chromadb

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

def get_collection(collection_name):
    if collection_name in client.list_collections():
        collection = client.get_collection(collection_name)
    else:
        collection = client.create_collection(collection_name)
    return collection

def add_to_collection(collection_name,documents):
    collection = get_collection(collection_name)
    collection.add(documents=documents)