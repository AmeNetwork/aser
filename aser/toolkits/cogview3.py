import requests
import os
from dotenv import load_dotenv
from aser.tools import tool

load_dotenv()


import requests


@tool()
def cogview3(prompt: str):
    """
    generate image with cogview3
    """
    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

    payload = {
        "model": "cogView-4-250304",
        "prompt": prompt,
        "size": "1024x1024",
        "watermark_enabled": False,
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('BIG_MODEL_API_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    response_json = response.json()
    image_url = response_json["data"][0]["url"]

    return image_url
