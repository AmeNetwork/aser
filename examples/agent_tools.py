from aser.tools import Tools
from aser.agent import Agent
tools=Tools()
def get_btc_price():
    return "$10,0000"

tools.add(
    name="get_bitcoin_price",
    description="when user ask bitcoin price, return bitcoin price",
    parameters=None,
    function=get_btc_price,
)

agent=Agent(name="aser",model="gpt-3.5-turbo",description="btc agent",tools=tools)

response=agent.chat("what is bitcoin price?")

