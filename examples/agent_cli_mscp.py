from aser.agent import Agent
from aser.cli import Cli
from aser.mscp import Chat2Web3
from aser.mscp import Connector
from eth_account import Account
import os

# Create a connector to connect to the component
component = Connector(
    "http://127.0.0.1:8545", # RPC of the component network
    "0x5b38CE75E7F755A2F6Fb4915C8A52B2d87Fd8ea0"  # component address
)

# Import the private key from the environment variable
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))

# Initialize Chat2Web3 object for handling blockchain interactions
chat2web3 = Chat2Web3(account)

# Get the methods of the component
methods = component.get_methods()

# Add methods to chat2web3
chat2web3.add(
    name="createContent",
    prompt="When a user wants to create a content on chainfeed, call this function",
    method=methods["createContent"],  
)
chat2web3.add(
    name="getRecentContent",
    prompt="When a user wants to get the recent content on chainfeed, call this function",
    method=methods["getRecentContent"],  
)

# Create an Agent instance
agent = Agent(name="aser agent", model="gpt-4.1-mini",chat2web3=chat2web3)

cli = Cli(agent)
cli.cmdloop()