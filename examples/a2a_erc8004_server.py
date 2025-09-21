from aser.agent import Agent
from aser.a2aser import A2Aser
from aser.tools import tool
from aser.utils.erc8004_extension import create_identity_extension
from eth_account import Account
import os


@tool()
def get_btc_price():
    """this function is used to get btc price"""
    return "100,000"


agent = Agent(
    name="aser agent",
    model="gpt-4.1-mini",
    description="this agent is used to get btc price",
    tools=[get_btc_price],
)

identity_extension = create_identity_extension(
    registrations=[
        {
            "agentId": 12345,
            "agentAddress": f"eip155:1:{Account.from_key(os.getenv("EVM_PRIVATE_KEY")).address}",
            "signature": "0x"
        }
    ],
    trustModels=["feedback"]
)

a2aser = A2Aser(agent, extensions=[identity_extension])
a2aser.run()
