import requests
import os
from dotenv import load_dotenv

load_dotenv()


import requests


def generate_image(prompt):
    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

    payload = {
        "model": "cogView-4-250304",
        "prompt": prompt,
        "size": "1024x1024",
        "watermark_enabled": False,
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('BIG_MODEL')}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    response_json = response.json()
    image_url = response_json["data"][0]["url"]

    return image_url



cogview3 = [
    {
        "name": "generate_image",
        "description": "when user want to generate image, use this tool",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "prompt to generate image",
                }
            },
            "required": ["prompt"],
        },
        "function": generate_image,
        "extra_prompt": None,
        "example": "generate image of a cat",
    }
]
