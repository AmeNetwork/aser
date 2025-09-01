from aser.agent import Agent
from aser.cli import Cli
from aser.mscp import Chat2Web3
from aser.mscp import Connector
from eth_account import Account
from aser.mcp import MCP
from aser.toolkits import web3bio
import os

# mscp
component = Connector(
    "http://127.0.0.1:8545", "0x5b38CE75E7F755A2F6Fb4915C8A52B2d87Fd8ea0"
)
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
chat2web3 = Chat2Web3(account)
methods = component.get_methods()
chat2web3.add(
    name="getRecentContent",
    prompt="When a user wants to get the recent content on chainfeed, call this function",
    method=methods["getRecentContent"],
)

# mcp
user_mcp = MCP("http://127.0.0.1:9000/mcp")

agent = Agent(
    name="aser agent",
    model="gpt-4.1-mini",
    chat2web3=chat2web3,
    tools=[web3bio],
    mcp=[user_mcp],
)

cli = Cli(agent)
cli.cmdloop()
