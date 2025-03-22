from amer.api import API
from amer.agent import Agent
agent=Agent(name="api-agent",model="gpt-3.5-turbo")
api=API(agent)
api.run()
