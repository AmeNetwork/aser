from aser import Agent, Team
from aser.tools import Tools

tools = Tools()


def get_coin_price():

    return "100,000"


get_btc_price_tool = tools.create(
    name="get_bitcoin_price",
    description="when user ask bitcoin price, return bitcoin price",
    parameters=None,
    function=get_coin_price,
)

agent_search = Agent(
    name="search_btc_agent",
    model="gpt-4o-mini",
    description="search bitcoin price",
    tools=[get_btc_price_tool],
)
agent_write = Agent(
    name="write_agent", description="write article", model="gpt-4.1-mini"
)
agent_supervisor = Agent(
    name="supervisor_agent", description="supervisor", model="gpt-4.1-mini"
)

agents = Team(name="agents_team", members=[agent_search, agent_write])
result = agents.run(
    mode="supervisor",
    task="get bitcoin price",
    supervisor=agent_supervisor,
)


print(result)
