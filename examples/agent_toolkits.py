from aser.toolkits import web3bio
from aser.agent import Agent
agent=Agent(name="token agent",model="gpt-4o-mini",tools=[web3bio])
response=agent.chat("who is vitalik.eth")
print(response)
