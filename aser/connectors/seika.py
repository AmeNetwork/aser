from web3 import Web3
from eth_account import Account
import os
import json
import time
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class CheckWork(BaseModel):
    verify: bool


class Seika:
    def __init__(self, _agent, _rpc, _contract, _account, _role, _interval):

        self.agent = _agent
        self.account = _account

        with open("aser/connectors/abi/seika_abi.json", "r", encoding="utf-8") as f:
            abi = json.load(f)
        self.web3 = Web3(Web3.HTTPProvider(_rpc))
        self.contract = self.web3.eth.contract(address=_contract, abi=abi)

        self.role = _role

        self.interval = _interval

        if _role == "worker":
            self.register_worker()

    def register_worker(self):

        agent = self.contract.functions.agents(self.account.address).call()

        if not agent[1]:
            agent_info = self.agent.get_info()
            agent_metadata = json.dumps(
                {
                    "name": agent_info["name"],
                    "description": agent_info["description"],
                },
                ensure_ascii=False,
            )

            estimated_txn = self.contract.functions.updateWorker(
                True, agent_metadata
            ).build_transaction(
                {
                    "from": self.account.address,
                    "value": 0,
                    "nonce": self.web3.eth.get_transaction_count(self.account.address),
                }
            )
            estimated_gas = self.web3.eth.estimate_gas(estimated_txn)
            gasPrice = self.web3.eth.gas_price
            txn = self.contract.functions.updateWorker(
                True, agent_metadata
            ).build_transaction(
                {
                    "from": self.account.address,
                    "nonce": self.web3.eth.get_transaction_count(self.account.address),
                    "gasPrice": gasPrice,
                    "gas": estimated_gas,
                }
            )
            signed_txn = self.account.sign_transaction(txn)
            txn_hash = self.web3.eth.send_raw_transaction(
                signed_txn.raw_transaction
            ).hex()

    def get_order(self):
        worker_order_ids = self.contract.functions.getOrderIdsByWorker(
            self.account.address
        ).call()
        order_ids_count = self.contract.functions.orderId().call()
        for i in range(order_ids_count):
            order_detail = self.contract.functions.orders(i).call()
            order = {
                "id": order_detail[0],
                "price": order_detail[1],
                "limit": order_detail[2],
                "description": order_detail[3],
                "publisher": order_detail[4],
                "date": order_detail[5],
                "status": order_detail[6],
            }
            if order["status"] == 1:
                if order_detail[0] not in worker_order_ids:
                    return order

    def submit_work(self, order_id, content):

        estimated_txn = self.contract.functions.createWork(
            order_id, content
        ).build_transaction(
            {
                "from": self.account.address,
                "value": 0,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
            }
        )
        estimated_gas = self.web3.eth.estimate_gas(estimated_txn)
        gasPrice = self.web3.eth.gas_price

        txn = self.contract.functions.createWork(order_id, content).build_transaction(
            {
                "from": self.account.address,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
                "gasPrice": gasPrice,
                "gas": estimated_gas,
            }
        )
        signed_txn = self.account.sign_transaction(txn)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction).hex()
        return txn_hash

    def check_work(self, work_id, agree):
        estimated_txn = self.contract.functions.checkWork(
            work_id, agree
        ).build_transaction(
            {
                "from": self.account.address,
                "value": 0,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
            }
        )
        estimated_gas = self.web3.eth.estimate_gas(estimated_txn)
        gasPrice = self.web3.eth.gas_price

        txn = self.contract.functions.checkWork(work_id, agree).build_transaction(
            {
                "from": self.account.address,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
                "gasPrice": gasPrice,
                "gas": estimated_gas,
            }
        )
        signed_txn = self.account.sign_transaction(txn)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction).hex()
        return txn_hash

    def get_order_work(self):

        order_ids = self.contract.functions.getOrderIdsByPublisher(
            self.account.address
        ).call()

        for id in order_ids:

            order = self.contract.functions.orders(id).call()
            order_id = order[0]
            order_detail = order[3]
            order_status = order[6]

            if order_status == 1:

                work_ids = self.contract.functions.getWorkIds(order_id).call()

                for work_id in work_ids:

                    work = self.contract.functions.works(work_id).call()

                    work_id = work[0]
                    work_detail = work[2]
                    work_status = work[4]

                    if work_status == 0:

                        return {
                            "order_id": order_id,
                            "order_detail": order_detail,
                            "work_id": work_id,
                            "work_detail": work_detail,
                        }

    def run(self):

        while True:

            if self.role == "reviewer":

                print("reviewer: query order")

                order_work = self.get_order_work()

                if order_work != None:

                    message = f"""
                        You are a verifier. Please verify whether it is correct

                        Question:{order_work["order_detail"]}

                        Answer:{order_work["work_detail"]}

                    """

                    response = self.agent.chat(message, response_format=CheckWork)

                    result = json.loads(response)["verify"]

                    self.check_work(order_work["work_id"], result)

            else:

                print("worker: query order")

                order = self.get_order()

                print("worker: order", order)

                if order != None:
                    message = order["description"]

                    response = self.agent.chat(message)

                    txn_hash = self.submit_work(order["id"], response)

            time.sleep(self.interval)
