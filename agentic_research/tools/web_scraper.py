import httpx
from bs4 import BeautifulSoup

def fetch_page(url):
    response = httpx.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)   
    return text