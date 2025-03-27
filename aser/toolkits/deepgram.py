import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.deepgram.com/v1/"
headers = {
    "Authorization": f"Token {os.getenv("DEEPGRAM_API_KEY")}",
    "Content-Type": "text/plain"
}

current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
audio_file_name=f"audio_{current_timestamp}.mp3"
path=f"data/audio/{audio_file_name}"

def text_to_speech(text, model="aura-asteria-en",path=path):   
    req_url = f"{url}speak?model={model}"
    response = requests.post(req_url, headers=headers, data=text)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)
        return path
    else:

        return f"fail: {response.status_code}"

deepgram = [
    {
        "name": "text_to_speech",
        "description": "convert text to speech",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "text to convert",
                }
            },
            "required": ["text"],
        },
        "function": text_to_speech,
        "extra_prompt": None,
        "example": "covert hello world to speech",
    }
]
      

