import requests
import os
from dotenv import load_dotenv
import uuid
load_dotenv()


def generate_image(prompt):
    url = "https://api.runware.ai/v1"
    headers = {
        "Content-Type": "application/json"
    }
    data = [
        {
            "taskType": "authentication",
            "apiKey": os.getenv("RUNWARE_KEY")
        },
        {
            "taskType": "imageInference",
            "taskUUID": str(uuid.uuid4()),
            "steps": 30,
            "positivePrompt": prompt,
            "width": 512,
            "height": 512,
            "model": "runware:101@1",
            "numberResults": 1,
            "outputFormat": "PNG",
            "outputType": [
                "URL"
            ],
        }
    ]
    response = requests.post(url, headers=headers, json=data)
    response_json=response.json()
    image_url=response_json["data"][0]["imageURL"]
    return image_url


runware = [
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
