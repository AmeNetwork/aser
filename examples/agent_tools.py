from aser.tools import Tools
from aser.agent import Agent


tools=Tools()
def get_btc_price():
    return "10,0000"

tools.add(
    name="get_bitcoin_price",
    description="when user ask bitcoin price, return bitcoin price",
    parameters=None,
    function=get_btc_price,
    strict=True
)

agent=Agent(name="aser",model="gpt-4o-mini",description="btc agent",tools=tools)

response=agent.chat("what is bitcoin price?")

print(response)

