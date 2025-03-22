from aser.agent import Agent
from aser.memory import Memory

memory = Memory(type="sqlite")
agent = Agent(
    name="aser agent", description="aser agent", model="gpt-3.5-turbo", memory=memory
)
response = agent.chat("What is Bitcoin?", uid=1)
print(response)
