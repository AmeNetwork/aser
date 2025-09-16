from aser import Evaluator
from aser.agent import Agent
from aser.tools import tool

evaluator = Evaluator()

@tool()
def get_coin_price():
    """get btc price"""
    return "100,000"

agent = Agent(name="aser agent",description="aser agent",model="gpt-4.1-mini",tools=[get_coin_price])

test_cases = [
    {"input": "get btc price", "expected": "100,000"},
]

results = evaluator.evaluate_agent(agent, test_cases)

print(results)