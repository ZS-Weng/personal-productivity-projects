import httpx
from bs4 import BeautifulSoup
import html2text
import os
from pathlib import Path

def fetch_page(url):
    response = httpx.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)   
    return text

def fetch_page_to_md(url, subfolder=None):
    h = html2text.HTML2Text()
    response = httpx.get(url)
    markdown = h.handle(response.text)
    base_path = Path("research")
    if subfolder:
        filename = base_path/f"{subfolder}/{url.split('/')[-2]}.md"
    else:
        filename = base_path/f"{url.split('/')[-2]}.md"
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
