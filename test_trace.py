from esper.trace import Trace
from esper.agent import Agent
from esper.tools import Tools
from esper.memory import Memory
from esper.chat2web3 import Chat2Web3
from dotenv import load_dotenv
import os
from eth_account import Account
from esper.ame.component import AmeComponent
load_dotenv()


private_key = os.getenv("EVM_PRIVATE_KEY")
account = Account.from_key(private_key)

chat2web3 = Chat2Web3("evm",account)
component = AmeComponent(
    "http://127.0.0.1:8545", "0x29a79095352a718B3D7Fe84E1F14E9F34A35598e"
)

methods = component.get_methods()



chat2web3 = Chat2Web3("evm", account)
chat2web3.add(
    "getUserNameByAddress",
    "when a user want to get user name and age, it will return 2 value, one is name, the one is age",
    methods["getUser"],
)

tools=Tools()
memory=Memory(type="sqlite")

def get_weather():

    return "sunny"

tools.add(
    name="get_weather",
    description="when user ask weather, return weather",
    parameters=None,
    function=get_weather,
)

trace=Trace(session="89795")
agent=Agent(name="test",model="gpt-3.5-turbo",description="test",trace=trace,memory=memory,tools=tools,chat2web3=chat2web3)
result = agent.chat("get user name 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")

# result=agent.chat("what is the weather today?",uid="1111")
print(result)

