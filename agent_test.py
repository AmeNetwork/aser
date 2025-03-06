from esper import Agent
from esper.ame import AmeComponent
from eth_account import Account
import os
from esper.chat2web3 import Chat2Web3

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

agent=Agent(name="test",description="test",model="x-ai/grok-2-vision-1212",chat2web3=chat2web3)
response=agent.chat("get user name 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")
print(response)

