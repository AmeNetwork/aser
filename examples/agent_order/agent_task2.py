from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

load_dotenv()
# from aser.agent import Agent
# agent=Agent(name="api-agent",model="gpt-3.5-turbo")

import json

with open("examples/agent_order/abi.json", "r", encoding="utf-8") as f:
    abi = json.load(f)
rpc = "http://127.0.0.1:8545"
contract_address = "0x82Dc47734901ee7d4f4232f398752cB9Dd5dACcC"
web3 = Web3(Web3.HTTPProvider(rpc))
contract = web3.eth.contract(address=contract_address, abi=abi)
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
publisher = Account.from_key(os.getenv("PUBLISHER_PRIVATE_KEY"))


def get_order():
    worker_order_ids = contract.functions.getOrderIdsByWorker(account.address).call()
    order_ids_count = contract.functions.orderId().call()
    for i in range(order_ids_count):
        order_detail = contract.functions.orders(i).call()
        order = {
            "id": order_detail[0],
            "price": order_detail[1],
            "limit": order_detail[2],
            "description": order_detail[3],
            "publisher": order_detail[4],
            "date": order_detail[5],
            "status": order_detail[6],
        }
        if order_detail[0] not in worker_order_ids:
            return order


def submit_work(order_id, content):

    estimated_txn = contract.functions.createWork(order_id, content).build_transaction(
        {
            "from": account.address,
            "value": 0,
            "nonce": web3.eth.get_transaction_count(account.address),
        }
    )
    estimated_gas = web3.eth.estimate_gas(estimated_txn)
    gasPrice = web3.eth.gas_price
    print(estimated_txn)
    txn = contract.functions.createWork(order_id, content).build_transaction(
        {
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gasPrice": gasPrice,
            "gas": estimated_gas,
        }
    )
    signed_txn = account.sign_transaction(txn)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction).hex()
    return txn_hash


def check_work(work_id, agree):
    estimated_txn = contract.functions.checkWork(work_id, agree).build_transaction(
        {
            "from": account.address,
            "value": 0,
            "nonce": web3.eth.get_transaction_count(account.address),
        }
    )
    estimated_gas = web3.eth.estimate_gas(estimated_txn)
    gasPrice = web3.eth.gas_price
    print(estimated_txn)
    txn = contract.functions.checkWork(work_id, agree).build_transaction(
        {
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gasPrice": gasPrice,
            "gas": estimated_gas,
        }
    )
    signed_txn = account.sign_transaction(txn)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction).hex()
    return txn_hash


def get_order_work():

    order_ids = contract.functions.getOrderIdsByPublisher(publisher.address).call()

    for id in order_ids:

        order = contract.functions.orders(id).call()
        order_id = order[0]
        order_detail = order[3]
        order_status = order[6]

        if order_status == 1:

            work_ids = contract.functions.getWorkIds(order_id).call()

            for work_id in work_ids:

                work = contract.functions.works(work_id).call()

                work_id = work[0]
                work_detail = work[2]
                work_status = work[4]

                if work_status == 0:

                    return {
                        order_id: order_id,
                        order_detail: order_detail,
                        work_id: work_id,
                        work_detail: work_detail,
                    }


# order_work = get_order_work()

# print(order_work)


# order=search_order()
# print(order)

# def timer(interval, func):
#     def wrapper():
#         func()
#         threading.Timer(interval, wrapper).start()
#     threading.Timer(interval, wrapper).start()


import time

def my_function():
    print("函数被调用了")

while True:
    my_function()
    time.sleep(3)


