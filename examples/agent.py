from esper.agent import Agent
from esper.memory import Memory

memory = Memory(type="sqlite")
agent = Agent(
    name="esper agent", description="esper agent", model="gpt-3.5-turbo", memory=memory
)
response = agent.chat("hello", uid=1)
print(response)
