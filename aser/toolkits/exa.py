import requests
import os
from dotenv import load_dotenv

load_dotenv()


def search(query):
    url = "https://api.exa.ai/search"
    headers = {
        "x-api-key": os.getenv("EXA_API_KEY"),
        "Content-Type": "application/json",
    }
    data = {"query": query, "text": True}
    response = requests.post(url, headers=headers, json=data)
    results = response.json()["results"]

    content = ""
    for result in results:
        content += f"title: {result.get('title', '')}\nurl: {result.get('url', '')}\n"

    return content


exa = [
    {
        "name": "search",
        "description": "search for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "query to search",
                }
            },
            "required": ["query"],
        },
        "function": search,
        "extra_prompt": None,
        "example": "search for latest research in LLMs",
    }
]
