# main.py - Entry point

from config import DEFAULT_MODEL
from llm_client import generate_response
from tools.web_scraper import fetch_page, fetch_page_to_md

def summarize_page():
    url = "https://www.mot.gov.sg/news-resources/newsroom/speech-by-acting-minister-for-transport-mr-jeffrey-siow-at-ministry-of-transport-s-committee-of-supply-debate-2026/"
    background = fetch_page(url)
    prompt = f"Based on the following text: {background},\n\nsummarize on the main points and key takeaways."
    response = generate_response(prompt)
    print(response)

def html_to_md(url):
    fetch_page_to_md(url, subfolder="budget_2026")
    
if __name__ == "__main__":
    # summarize_page()
    list_url = ["https://www.mot.gov.sg/news-resources/newsroom/speech-by-minister-of-state-for-transport-mr-baey-yam-keng-at-ministry-of-transport-s-committee-of-supply-debate-2026/",
                "https://www.mot.gov.sg/news-resources/newsroom/speech-by-senior-minister-of-state-for-transport--ms-sun-xueling-at-ministry-of-transport-s-committee-of-supply-debate-2026/",
                "https://www.mot.gov.sg/news-resources/newsroom/speech-by-senior-minister-of-state-for-transport-and-law-mr-murali-pillai-at-ministry-of-transport-s-committee-of-supply-2026-debate/"]

    for url in list_url:
        html_to_md(url)