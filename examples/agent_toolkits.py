from amer.tools import Tools
from amer.toolkits import erc20
from amer.agent import Agent
tools=Tools()
tools.load_toolkits([erc20])
agent=Agent(name="token agent",model="gpt-3.5-turbo")
response=agent.chat("deploy a erc20 token, name is binance, symbol is bnb")

