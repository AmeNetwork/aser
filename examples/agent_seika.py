import os
import threading
from dotenv import load_dotenv
from eth_account import Account
from aser.tools import Tools
from aser.toolkits import cast
from aser.connectors import Seika
from aser.agent import Agent

load_dotenv()
rpc = "http://127.0.0.1:8545"
contract_address = "0x3A1D75769758705caB1385377d4D88b8193A5f37"
worker_account = Account.from_key(os.getenv("WORKER_AGENT_PRIVATE_KEY"))
reviewer_account = Account.from_key(os.getenv("REVIEWER_AGENT_PRIVATE_KEY"))

tools = Tools()
tools.load_toolkits([cast])
worker_agent = Agent(name="worker agent", model="gpt-4o-mini", tools=tools)

reviewer_agent = Agent(name="reviewer agent", model="gpt-4o-mini")

worker_agent_task = Seika(
    worker_agent, rpc, contract_address, worker_account, "worker", 5
)
reviewer_agent_task = Seika(
    reviewer_agent, rpc, contract_address, reviewer_account, "reviewer", 5
)


worker_thread = threading.Thread(target=worker_agent_task.run)
reviewer_thread = threading.Thread(target=reviewer_agent_task.run)

worker_thread.start()
reviewer_thread.start()

worker_thread.join()
reviewer_thread.join()
