from aser.tools import tool
import os
import json
import requests
@tool
def gopher_twitter(query: str, max_results: int = 10):
    """this function is used to search gopher twitter or X"""

    url = "https://data.gopher-ai.com/api/v1/search/live/"
    headers = {
        "Authorization": f"Bearer {os.getenv('GOPHER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "twitter",
        "arguments": {
            "type": "searchbyquery",
            "query": query,
            "max_results": max_results
        }
    }
    response = requests.post(url, headers=headers, json=data)

    return json.dumps(response.json())

gopher=[gopher_twitter]