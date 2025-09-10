from aser.api import API
from aser.agent import Agent

agent = Agent(
    name="api-agent",
    description="aser",
    avatar="https://i.postimg.cc/RVRP4BV6/aser-avatar.gif",
    model="gpt-4o-mini",
)


api = API(agent)
api.run()
