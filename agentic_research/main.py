# main.py - Entry point

from config import DEFAULT_MODEL
from config import RESEARCH_DIR
from llm_client import generate_response
from tools.web_scraper import fetch_page, fetch_page_to_md
from tools.local_search import load_knowledge_base
from tools.chunker import chunk_text
from tools.vector_store import get_collection, add_to_collection

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

def add_collection(path=RESEARCH_DIR/'budget_2026'):
    knowledge_base = load_knowledge_base(path=path)
    collection = get_collection(path.name)
    for title, doc in knowledge_base.items():
        chunks = chunk_text(doc['content'])
        documents = [{"id": f"{title}_{i}", 
                      "text": chunk,
                      "metadata": {"title": title, "sub_folder": path.name, "id": f"{id}"}} for i, chunk in enumerate(chunks)]
        add_to_collection(collection, documents)
        

if __name__ == "__main__":
    fetch_knowledge_base()