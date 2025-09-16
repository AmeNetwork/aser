from aser import Agent, Team
from aser.tools import tool
import asyncio


@tool()
def get_btc_price():
    """get bitcoin or btc price"""
    return "100,000"


@tool()
def get_eth_price():
    """get eth or ethereum price"""
    return "1,000"


@tool()
def get_sol_price():
    """get solana or sol price"""
    return "100"


agent_btc = Agent(
    name="search_btc_agent",
    model="gpt-4o-mini",
    description="search bitcoin price",
    tools=[get_btc_price],
)
agent_eth = Agent(
    name="search_eth_agent",
    model="gpt-4o-mini",
    description="search ethereum price",
    tools=[get_eth_price],
)
agent_sol = Agent(
    name="search_sol_agent",
    model="gpt-4o-mini",
    description="search solana price",
    tools=[get_sol_price],
)
agent_write = Agent(
    name="write_agent", description="write article, max 100 words", model="gpt-4.1-mini"
)
supervisor = Agent(
    name="supervisor_agent", description="supervisor", model="gpt-4.1-mini"
)

agents = Team(
    name="agents_team",
    members=[agent_btc, agent_eth, agent_sol, agent_write],
    supervisor=supervisor,
    mode="hierarchical",
)

async def main():
    result = await agents.run("write a article about crypto price")

    print(result["final_result"])


if __name__ == "__main__":
    asyncio.run(main())

