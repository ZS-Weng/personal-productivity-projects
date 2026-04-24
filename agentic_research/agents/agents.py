import json
from google import genai
import config
from agents.agent_tools import search_knowledge_base

client = genai.Client()          
def run_agent(user_query: str, max_steps: int = 5):
    messages = [{"role": "user", "content": user_query}]
    
    for step in range(max_steps):
        response = llm.call_with_tools(messages, tools=TOOL_SCHEMAS)
        
        if response.is_final_answer:
            return response.content
            
        # LLM chose a tool — execute it
        tool_result = execute_tool(response.tool_name, response.tool_args)
        
        # Feed result back
        messages.append({"role": "tool", "content": tool_result})
    
    return "Max steps reached"