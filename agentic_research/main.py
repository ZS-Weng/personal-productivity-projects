# main.py - Entry point

from config import DEFAULT_MODEL
from config import RESEARCH_DIR
from llm_client import generate_response
from tools.web_scraper import fetch_page, fetch_page_to_md
from tools.local_search import load_knowledge_base
from tools.chunker import chunk_text
from tools.vector_store import get_collection, add_to_collection, delete_collection

def summarize_page():
    url = "https://www.mot.gov.sg/news-resources/newsroom/speech-by-acting-minister-for-transport-mr-jeffrey-siow-at-ministry-of-transport-s-committee-of-supply-debate-2026/"
    background = fetch_page(url)
    prompt = f"Based on the following text: {background},\n\nsummarize on the main points and key takeaways."
    response = generate_response(prompt)
    print(response)

def html_to_md(url):
    fetch_page_to_md(url, subfolder="budget_2026")

def fetch_knowledge_base(path=RESEARCH_DIR/'budget_2026'):
    knowledge_base = load_knowledge_base(path=path)
    return knowledge_base

def collection_full_refresh(path=RESEARCH_DIR/'budget_2026'):
    knowledge_base = load_knowledge_base(path=path)
    collection_name = path.name
    delete_collection(collection_name)
    for title, doc in knowledge_base.items():
        chunks = chunk_text(doc)
        ids = [f"{title}_{i}" for i, chunk in enumerate(chunks)]
        documents = [chunk for i, chunk in enumerate(chunks)]
        metadatas = [{"title": title, "sub_folder": path.name, "chunk_index": i} for i, chunk in enumerate(chunks)]
        add_to_collection(collection_name, ids=ids, documents=documents, metadatas=metadatas)
def query_knowledge_base(query, collection_name):
    collection = get_collection(collection_name)
    results = collection.query(query_texts=[f"{query}"], n_results=3)
    prompt = f"Based on the following context: {results},\n\nanswer the question: {query}"
    response = generate_response(prompt)
    print(response)
        
if __name__ == "__main__":
    query_knowledge_base("What are the key opportunities as one of the transport operators in Singapore?", "budget_2026")
    # collection_full_refresh(path=RESEARCH_DIR/'budget_2026')
