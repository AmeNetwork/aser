from aser import Agent
from aser.mscp import Connector
from eth_account import Account
import os
from aser.mscp import Chat2Web3

# Create a connector to connect to the component
component = Connector(
    "http://127.0.0.1:8545", # RPC of the component network
    "0x29a79095352a718B3D7Fe84E1F14E9F34A35598e"  # component address
)

# Get the methods of the contract
methods = component.get_methods()

#Import the private key from the environment variable
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))

# Initialize Chat2Web3 object for handling blockchain interactions
chat2web3 = Chat2Web3(account)

# Add a method named "getUserInfoByAddress" to chat2web3
chat2web3.add(
    name="getUserInfoByAddress",
    prompt="When a user wants to get a user's name and age, it will return 2 values: one is the name, and the other is the age.",
    method=methods["getUser"],  # Use the getUser method from the contract
)

# Create an Agent instance
agent = Agent(
    name="chat2web3",  # Agent name
    model="gpt-4o",  # Specify the model to use
    chat2web3=chat2web3  # Use the previously created chat2web3 object
)

# Agent responds with final answer
response = agent.chat("What is the user's name and age?0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")

print(response)