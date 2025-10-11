from aser.utils import load_character
from aser.agent import Agent
character=load_character("./examples/character.json")
agent = Agent(name="aser agent", description="aser agent",
              model="gpt-4.1-mini",
              character=character
              )
response = agent.chat("can you introduce yourself?")
print(response)