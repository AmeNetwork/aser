from aser.toolkits import cast
from aser.agent import Agent


agent = Agent(name="token agent", model="gpt-4o-mini",tools=[cast])
response = agent.chat(
    "write a post about bitcoin and post it to farcaster"
)
print(response)
