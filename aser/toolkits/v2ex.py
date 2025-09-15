import requests
import os
from dotenv import load_dotenv

from aser.tools import tool

@tool()
def v2ex():
    """get latest topics on v2ex"""
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



