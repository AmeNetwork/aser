import os
from dotenv import load_dotenv
from eth_account import Account

load_dotenv()
from agent_task import AgentTask
from aser.agent import Agent

rpc = "http://127.0.0.1:8545"
contract_address = "0x82Dc47734901ee7d4f4232f398752cB9Dd5dACcC"
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
publisher = Account.from_key(os.getenv("PUBLISHER_PRIVATE_KEY"))
agent = Agent(name="agent", model="gpt-4o-mini")

agent_task = AgentTask(agent, rpc, contract_address, publisher, "publisher")

# agent_task = AgentTask(agent, rpc, contract_address, account, "worker")

agent_task.run()