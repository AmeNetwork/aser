from aser.tools import Tools
from aser.agent import Agent


tools=Tools()

def get_btc_price(arguments):
    return "100,000"

get_btc_price_tool=tools.create(
    name="get_bitcoin_price",
    description="when user ask bitcoin price, return bitcoin price",
    parameters=None,
    function=get_btc_price
)

agent=Agent(name="aser",model="gpt-4o-mini",description="btc agent",tools=[get_btc_price_tool])

response=agent.chat("what is bitcoin price?")

print(response)

