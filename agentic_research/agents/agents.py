import json
from google import genai
import config
from agents.agent_tools import search_knowledge_base

client = genai.Client()          
def run_agent(user_query: str, max_steps: int = 5):
    """Run the agent on a user query and return the final answer
    # 1. Call client.models.generate_content(...)
    # 2. Pass the model, the user_query, and the tool in config
    # 3. Return the .text from the response
    """

    response = client.models.generate_content(
    model=config.DEFAULT_MODEL,                    # hint: config.DEFAULT_MODEL
    contents=user_query,                 # hint: the user's question
    config={
        "tools": [search_knowledge_base]            # hint: the tool function you just wrote
        }
    )
    return response.text


def run_agent_manual(user_query: str, max_steps: int = 5) -> str:
    """Manual agent loop — we handle each tool call ourselves."""
    
    # 1. Initialise messages with the user's query
    messages = [
    {"role": "user", "parts": [{"text": user_query}]}
    ]
    
    # 2. Loop up to max_steps times
    for step in range(max_steps):
        # a. Call the LLM with current messages + tools
        # b. Check if it returned a tool call or a final answer
        # c. If tool call → execute it, append result to messages
        # d. If final answer → return it
        ...
    
    return "Max steps reached without final answer."