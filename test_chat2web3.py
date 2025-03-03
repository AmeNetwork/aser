from core.chat2web3 import Chat2Web3
from core.ame.ame_component import AmeComponent
from web3 import Web3
from eth_account import Account
from core.esper import Esper
import os
from core.memory import Memory
from dotenv import load_dotenv
from core.tools import Tools

load_dotenv()


component = AmeComponent(
    "http://127.0.0.1:8545", "0x29a79095352a718B3D7Fe84E1F14E9F34A35598e"
)

methods = component.get_methods()
private_key = os.getenv("EVM_PRIVATE_KEY")
account = Account.from_key(private_key)


chat2web3 = Chat2Web3("evm", account)
chat2web3.add(
    "getUserNameByAddress",
    "when a user want to get user name and age, it will return 2 value, one is name, the one is age",
    methods["getUser"],
)

# chat2web3.add(
#     "changeUserNameByAddress", "when a user change his name", methods["updateUserName"]
# )


# memory=Memory(type="tinydb",limit=3)
# gpt-4o , deepseek-chat

# result = esper.chat("hello","mayun")

# result = esper.chat("get user name 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")
# print(result)
# result = esper.chat("change my name,tina,0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")
tools = Tools()


def getWeather(city):
    return "sunny"


tools.add(
    "getWeather",
    "when a user want to get weather",
    getWeather,
    {
        "type": "object",
        "properties": {"city": {"type": "string"}},
    },
)


esper = Esper(name="robot1", description="test", model="gpt-4o",chat2web3=chat2web3,tools=tools)

result=esper.chat("get weather in shanghai")
print(result)