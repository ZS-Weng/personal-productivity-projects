# main.py - Entry point

from config import DEFAULT_MODEL
from llm_client import LLMClient

def main():
    client = LLMClient()
    response = client.generate("Hello, world!")
    print(response)

if __name__ == "__main__":
    main()