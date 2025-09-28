from aser.toolkits.recall import recall
from aser.agent import Agent
agent = Agent(
    name="token agent",
    model="gpt-4o-mini",
    tools=[recall],
)
balance_response = agent.chat(
    "get my balances"
)
print(balance_response)
trade_response = agent.chat(
    "execute a trade from 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 to 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 with amount 0.00001"
)
print(trade_response)
