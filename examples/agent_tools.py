from aser.tools import tool
from aser.agent import Agent

# You have 2 ways to create tools:
# 1. You can define tool with decorator
# 2. You can define tool with dict


# decorator
@tool
def get_btc_price():
    """this function is used to get btc price"""
    return "100,000"


@tool
def get_user_age(user_name: str):
    """this function is used to get user age"""
    if user_name == "alice":
        return "18"
    elif user_name == "bob":
        return "20"
    return f"user {user_name} age is not found"


#dict
def get_eth_price():
    return "1,000"


get_eth_price_tool = {
    "name": "get_eth_price",
    "description": "when user ask eth price, return eth price",
    "parameters": None,
    "function": get_eth_price,
}


agent = Agent(
    name="token agent",
    model="gpt-4o-mini",
    tools=[get_btc_price, get_user_age, get_eth_price_tool],
)
btc_tool_response = agent.chat("get btc price")
print(btc_tool_response)

user_age_tool_response = agent.chat("get alice age")
print(user_age_tool_response)

eth_tool_response = agent.chat("get eth price")
print(eth_tool_response)

