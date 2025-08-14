import os
import threading
from dotenv import load_dotenv
from eth_account import Account

load_dotenv()
from aser.connectors import Seika
from aser.agent import Agent

rpc = "http://127.0.0.1:8545"
contract_address = "0x5B3120d0dA5FDcBA7aef87A9c3c64829C1c0D76B"
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
publisher = Account.from_key(os.getenv("PUBLISHER_PRIVATE_KEY"))

agent = Agent(name="agent", model="gpt-4o-mini")

publisher_agent_task = Seika(agent, rpc, contract_address, publisher, "publisher",5)

worker_agent_task = Seika(agent, rpc, contract_address, account, "worker",5)


worker_thread = threading.Thread(target=worker_agent_task.run)
publisher_thread = threading.Thread(target=publisher_agent_task.run)


worker_thread.start()
publisher_thread.start()