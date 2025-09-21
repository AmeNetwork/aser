from aser import Agent
from mscp import Chat2Web3
from mscp.connectors.erc8004 import ERC8004IdentityConnector
from eth_account import Account
import os
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
identity_connector = ERC8004IdentityConnector(
    "http://127.0.0.1:8545",
    "0x3999761dD55a949Fa01878d6F31b2618f06DA0c1",
    account
)
chat2web3 = Chat2Web3([identity_connector])
agent = Agent(name="chat2web3", model="gpt-4o", chat2web3=chat2web3)
response = agent.chat(
    f"""
    create a newAgent
    agentDomain: http://www.ame.network
    agentAddress: {account.address}"""
)
print(response)
