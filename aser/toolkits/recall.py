import requests
from dotenv import load_dotenv
import os
from aser.tools import tool
import json

load_dotenv()


class TradingClient:
    def __init__(self, base_url, api_key):
        self.client = requests.Session()
        self.client.headers.update(
            {"Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"}
        )
        self.base_url = base_url

    def get_balances(self):
        response = self.client.get(f"{self.base_url}/agent/balances")
        return json.dumps(response.json())

    def execute_trade(
        self, from_token, to_token, amount, from_chain=None, to_chain=None
    ):
        trade = {
            "fromToken": from_token,
            "toToken": to_token,
            "amount": str(amount),
            "fromChain": from_chain,
            "toChain": to_chain,
            "reason": f"Buying {from_token} with {to_token}",
        }

   

        try:
            response = self.client.post(
                f"{self.base_url}/trade/execute", json=trade)
            if response.status_code != 200:
                raise Exception(
                    f"Trade failed: {response.json()['error']['message']}"
                )
            
            return json.dumps(response.json())
        except requests.exceptions.RequestException as error:
            if error.response:
                raise Exception(
                    f"Trade failed: {error.response.json()['error']['message']}"
                )
            raise error

    def get_token_price(self, token_address, chain=None, specific_chain=None):
        params = {
            "token": token_address,
            "chain": chain,
            "specificChain": specific_chain,
        }
        response = self.client.get(f"{self.base_url}/price", params=params)
        return json.dumps(response.json())

    def get_leaderboard(self):
        response = self.client.get(f"{self.base_url}/competition/leaderboard")
        return json.dumps(response.json())


trade_client = TradingClient(base_url=os.getenv(
    "RECALL_BASE_URL"), api_key=os.getenv("RECALL_API_KEY"))


@tool()
def get_balances():
    """Get the portfolio of the agent."""
    return trade_client.get_balances()


@tool()
def execute_trade(from_token: str, to_token: str, amount: str, from_chain=None, to_chain=None):
    """Execute a trade."""
    return trade_client.execute_trade(from_token, to_token, amount, from_chain, to_chain)


recall = [get_balances, execute_trade]





