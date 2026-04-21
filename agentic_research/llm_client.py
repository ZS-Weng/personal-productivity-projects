# llm_client.py - Abstraction layer for LLM APIs
import config
from google import genai

# Configure the API key
client = genai.Client()

def generate_response(prompt,model=config.DEFAULT_MODEL):
    response = client.models.generate_content(
    model=model, contents=prompt
    )
    return response.text
