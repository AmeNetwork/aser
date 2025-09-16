from aser import Agent, Team
from aser.tools import tool

@tool()
def get_coin_price():
    """get btc price"""
    return "100,000"

agent_search = Agent(
    name="search_btc_agent",
    model="gpt-4o-mini",
    description="search bitcoin price",
    tools=[get_coin_price],
)
agent_write = Agent(
    name="write_agent", description="write article", model="gpt-4.1-mini"
)
agent_supervisor = Agent(
    name="supervisor_agent", description="supervisor", model="gpt-4.1-mini"
)

agents = Team(name="agents_team", members=[agent_search, agent_write], supervisor=agent_supervisor, mode="reactive")
result = agents.run("write a report about bitcoin price")


print(result)
