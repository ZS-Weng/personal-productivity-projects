# main.py - Entry point

from config import DEFAULT_MODEL
from llm_client import generate_response
from tools.web_scraper import fetch_page, fetch_page_to_md
from tools.local_search import load_knowledge_base

def summarize_page():
    url = "https://www.mot.gov.sg/news-resources/newsroom/speech-by-acting-minister-for-transport-mr-jeffrey-siow-at-ministry-of-transport-s-committee-of-supply-debate-2026/"
    background = fetch_page(url)
    prompt = f"Based on the following text: {background},\n\nsummarize on the main points and key takeaways."
    response = generate_response(prompt)
    print(response)

def html_to_md(url):
    fetch_page_to_md(url, subfolder="budget_2026")

def fetch_knowledge_base():
    knowledge_base = load_knowledge_base()
    for title, content in knowledge_base.items():
        print(f"Title: {title}\nContent: {content[:200]}...\n")
    
if __name__ == "__main__":
    # # summarize_page()
    # list_url = [
    #     "https://www.mddi.gov.sg/newsroom/speech-by-sms-tan-kiat-how-at-the-committee-of-supply-debate-2026/",
    #     "https://www.mddi.gov.sg/newsroom/speech-by-mos-jasmin-lau-at-the-committee-of-supply-debate-2026/",
    #     "https://www.mddi.gov.sg/newsroom/-speech-by-mos-rahayu-mahzam-at-the-committee-of-supply-debate-2026/",
    #     "https://www.mddi.gov.sg/newsroom/speech-by-minister-josephine-teo-at-the-committee-of-supply-debate-2026/",
    # ]

    # for url in list_url:
    #     html_to_md(url)
    fetch_knowledge_base()