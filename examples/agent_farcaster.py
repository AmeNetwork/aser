from aser.tools import Tools
from aser.toolkits import cast
from aser.agent import Agent

tools = Tools()
tools.load_toolkits([cast])
agent = Agent(name="token agent", model="gpt-4o-mini",tools=tools)
response = agent.chat(
    "write a post about sei network and post it to farcaster"
)
print(response)
