from esper.tools import Tools
from esper.toolkits import erc20
from esper.agent import Agent
tools=Tools()
tools.load_toolkits([erc20])
agent=Agent(name="token agent",model="gpt-3.5-turbo")
response=agent.chat("deploy a erc20 token, name is binance, symbol is bnb")

