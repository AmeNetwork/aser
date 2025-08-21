import requests
import json


def get_web3_profile(identity):
    url = f"https://api.web3.bio/profile/{identity}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.dumps(response.json())
        return data
    else:
        return f"Identity {identity} not found"


web3bio = [
    {
        "name": "web3bio",
        "description": "get web3 profile of identity or who is, eg: vitalik.eth,0xd8da6bf26964af9d7eed9e03e53415d37aa96045,tony.base.eth,dwr.eth.farcaster,stani.lens",
        "parameters": {
            "type": "object",
            "properties": {
                "identity": {
                    "type": "string",
                    "description": "eg: vitalik.eth,0xd8da6bf26964af9d7eed9e03e53415d37aa96045,tony.base.eth,dwr.eth.farcaster,stani.lens",
                }
            },
            "required": ["identity"],
        },
        "function": get_web3_profile,
        "extra_prompt": None,
        "example": "get web3bio profile of vitalik.eth",
    }
]
