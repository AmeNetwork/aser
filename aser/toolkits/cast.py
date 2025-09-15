from aser.social.farcaster import FarcasterClient
from aser.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()

@tool()
def cast(farcaster_message:str):
    """
    post a cast on farcaster
    """
    farcaster_client=FarcasterClient(mnemonic=os.getenv("FARCASTER_MNEMONIC"))
    result=farcaster_client.post(farcaster_message)
    url=f"https://farcaster.xyz/{result["cast"]["author"]["username"]}/{result["cast"]["hash"]}"
    # content=result["cast"]["text"]
    return url

