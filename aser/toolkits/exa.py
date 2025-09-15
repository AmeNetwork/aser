import requests
import os
from dotenv import load_dotenv
from aser.tools import tool
load_dotenv()

@tool()
def exa(query:str):
    """search for information"""
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


