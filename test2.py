from esper import Chat2Web3
from esper.ame.component import AmeComponent
from esper import Agent
from eth_account import Account
import os
component = AmeComponent(
    "http://127.0.0.1:8545", "0x29a79095352a718B3D7Fe84E1F14E9F34A35598e"
)

methods = component.get_methods()

# from dotenv import load_dotenv
# load_dotenv()

account=Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
chat2web3 = Chat2Web3("evm",account)
chat2web3.add(
    "getUserNameByAddress",
    "when a user want to get user name and age, it will return 2 value, one is name, the one is age",
    methods["getUser"],
)

agent=Agent(name="jack",model="gpt-4",description="a chatbot",chat2web3=chat2web3)

result=agent.chat("get user name 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")
print(result)