from aser.social.farcaster import FarcasterClient
import os
from dotenv import load_dotenv
load_dotenv()
farcaster_client=FarcasterClient(mnemonic=os.getenv("FARCASTER_MNEMONIC"))

def farcaster_cast(farcaster_message):
    result=farcaster_client.post(farcaster_message)
    url=f"https://farcaster.xyz/{result["cast"]["author"]["username"]}/{result["cast"]["hash"]}"
    # content=result["cast"]["text"]
    return url

cast = [
    {
        "name": "farcaster_cast",
        "description": "When the user asks you to send a cast or content in the forecaster.",
        "parameters": {
            "type": "object",
            "properties": {
                "farcaster_message": {
                    "type": "string",
                    "description": "farcaster message, no more than 500 characters",
                }
            },
            "required": ["farcaster_message"],
        },
        "function": farcaster_cast,
        "extra_prompt": None,
        "example":None,
    }
]