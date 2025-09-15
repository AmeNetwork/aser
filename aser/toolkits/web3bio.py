import requests
import json
from aser.tools import tool
@tool()
def web3bio(identity:str):
    """get web3 profile of identity or who is, eg: vitalik.eth,0xd8da6bf26964af9d7eed9e03e53415d37aa96045,tony.base.eth,dwr.eth.farcaster,stani.lens"""
    url = f"https://api.web3.bio/profile/{identity}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.dumps(response.json())
        return data
    else:
        return f"Identity {identity} not found"


