from aser import Agent
from mscp import Chat2Web3
from mscp.connectors.erc7654 import ERC7654Connector
from eth_account import Account
import os

component_connector = ERC7654Connector(
    "http://127.0.0.1:8545",
    "0x0E2b5cF475D1BAe57C6C41BbDDD3D99ae6Ea59c7",  
    Account.from_key(os.getenv("EVM_PRIVATE_KEY")) 
)
chat2web3 = Chat2Web3([component_connector])
agent=Agent(name="chat2web3",model="gpt-4o",chat2web3=chat2web3)
response = agent.chat("What is the user's name and age?0x8241b5b254e47798E8cD02d13B8eE0C7B5f2a6fA")

print(response)
