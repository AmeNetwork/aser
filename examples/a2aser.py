from aser.agent import Agent
from aser.a2aser import A2Aser
from aser.tools import tool

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

a2aser = A2Aser(agent)



