from aser.toolkits import web3bio
from aser.agent import Agent

agent = Agent(name="token agent", model="gpt-4o-mini", tools=[web3bio])
response = agent.chat(
    "who is 0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
)
print(response)
