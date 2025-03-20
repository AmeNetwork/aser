import requests
import json

defillama_url="https://api.llama.fi/"
def get_tvl(protocol):
    
    response = requests.get(f"{defillama_url}tvl/{protocol}")
    
    if response.status_code == 200:
        return f"TVL: {response.json()}"
    else:
        return "Not found"

def get_volume(protocol):

    response = requests.get(f"{defillama_url}summary/dexs/{protocol}?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyVolume")

    if response.status_code == 200:

        response_json=response.json()

        return f"""
        Name: {response_json["name"]}
        Description: {response_json["description"]}
        Total 24h Volume: {response_json["total24h"]:,}
        Total 7d Volume: {response_json["total7d"]:,}
        Total All Time: {response_json["totalAllTime"]:,}
        """
        
    else:
        return "Not found"



defillama = [
    {
        "name": "get_tvl",
        "description": "get tvl by protocol name",
        "parameters": {
            "type": "object",
            "properties": {
                "protocol": {
                    "type": "string",
                    "description": "protocol name",
                }
            },
            "required": ["protocol"],
        },
        "function": get_tvl,
        "extra_prompt": None,
        "example":"get tvl of uniswap"
    }, {
        "name": "get_volume",
        "description": "get volume by protocol name",
        "parameters": {
            "type": "object",
            "properties": {
                "protocol": {
                    "type": "string",
                    "description": "protocol name",
                }
            },
            "required": ["protocol"],
        },
        "function": get_volume,
        "extra_prompt": None,
        "example":"get volume of uniswap"
    }
]


