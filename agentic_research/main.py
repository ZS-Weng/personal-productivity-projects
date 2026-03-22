# main.py - Entry point

from config import DEFAULT_MODEL
from llm_client import generate_response

def main():
    prompt = "What is the origin of the Python programming language?"
    response = generate_response(prompt)
    print(response)

if __name__ == "__main__":
    main()