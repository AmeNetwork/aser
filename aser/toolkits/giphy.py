"""https://developers.giphy.com/"""
import os
from dotenv import load_dotenv
import json
from urllib import parse, request
from aser.tools import tool

load_dotenv()


@tool()
def giphy(query: str):
    """this function is used to search gif image url"""
    GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
    url = "http://api.giphy.com/v1/gifs/search"
    params = parse.urlencode({
    "q": query,
    "api_key": GIPHY_API_KEY,
    "limit": "1"
    })
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())
        imgs=[]
        for item in data["data"]:
            imgs.append(item["url"])

        return json.dumps(imgs)



