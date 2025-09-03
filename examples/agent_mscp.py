from aser import Agent
from mscp import Connector,Chat2Web3


from eth_account import Account
import os


# Create a connector to connect to the component
component_connector = Connector(
    "http://127.0.0.1:8545", # RPC of the component network
    "0x0E2b5cF475D1BAe57C6C41BbDDD3D99ae6Ea59c7",  # component address
    Account.from_key(os.getenv("EVM_PRIVATE_KEY")) # Account
)

# Initialize Chat2Web3 
chat2web3 = Chat2Web3([component_connector])



# Agent responds with final answer
agent=Agent(name="chat2web3",model="gpt-4o",chat2web3=chat2web3)
response = agent.chat("What is the user's name and age?0x8241b5b254e47798E8cD02d13B8eE0C7B5f2a6fA")

print(response)