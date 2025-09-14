import requests
import os
from dotenv import load_dotenv


def get_v2ex_latest():

    url = f"https://www.v2ex.com/api/topics/latest.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        content = ""
        for item in data:
            content += f"title: {item.get('title', '')}\n url: {item.get('url', '')}\n content:{item.get('content', '')}\n"

        return content
    else:
        return None


v2ex = [
    {
        "name": "get_v2ex_latest",
        "description": "get latest topics on v2ex",
        "parameters": None,
        "function": get_v2ex_latest,
        "extra_prompt": None,
        "example": "get latest topics on v2ex",
    }
]
