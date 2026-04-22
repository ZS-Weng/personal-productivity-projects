import json
from google import genai
import config
from tools.vector_store import get_collection, query_collection

def search_knowledge_base(query: str, collection_name: str) -> str:
    """
    Searches a local knowledge base of research articles stored in ChromaDB
    collections to retrieve the most relevant chunks for a given query.

    Args:
        query (str): The natural language question or search text to look up.
            The tool performs semantic similarity search against the chosen
            collection and returns the top matching chunks.

        collection_name (str): The name of the ChromaDB collection to search.
            Available collections:
            - "budget_2026": Singapore Government's Budget 2026 plans across
              key ministries, based on the Committee of Supply speeches.
              Useful for questions about Singapore's national direction,
              ministry priorities, and policy announcements for 2026.

    Returns:
        str: The top matching chunks from the specified collection, which
        can be used as context to answer the user's question.
    """
    # call query_vector_store and return the result
    results = query_collection(query, collection_name)
    return results

query = "What is the key highlights of Ministry of Transport for 2026?"
search_knowledge_base(query, "budget_2026")