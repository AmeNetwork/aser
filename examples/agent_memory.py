from amer.agent import Agent
from amer.memory import Memory

memory = Memory(type="sqlite")
agent = Agent(
    name="amer agent", description="amer agent", model="gpt-3.5-turbo", memory=memory
)
response = agent.chat("What is Bitcoin?", uid=1)
print(response)
