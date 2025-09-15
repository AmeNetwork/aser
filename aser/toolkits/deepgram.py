import requests
import datetime
import os
from dotenv import load_dotenv
from aser.tools import tool

load_dotenv()

url = "https://api.deepgram.com/v1/"
headers = {
    "Authorization": f"Token {os.getenv("DEEPGRAM_API_KEY")}",
    "Content-Type": "text/plain",
}

current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
audio_file_name = f"audio_{current_timestamp}.mp3"
path = f"data/audio/{audio_file_name}"


@tool()
def deepgram(text: str, model: str = "aura-asteria-en", path: str = path):
    """
    convert text to speech
    """

    req_url = f"{url}speak?model={model}"
    response = requests.post(req_url, headers=headers, data=text)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)
        return f"audio file saved at {path}"
    else:

        return f"fail: {response.status_code}"
