import requests
import json
from aser.tools import tool
defillama_url="https://api.llama.fi/"

@tool()
def get_tvl(protocol:str):
    """get tvl by protocol name, protocol is necessary"""
    response = requests.get(f"{defillama_url}tvl/{protocol}")
    
    if response.status_code == 200:
        return f"TVL: {response.json()}"
    else:
        return "Not found"

@tool()
def get_volume(protocol:str):
    """get volume by protocol name, protocol is necessary"""
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
    get_tvl,
    get_volume
]


