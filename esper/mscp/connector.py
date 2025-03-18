from esper.mscp.lib import get_data_types
from web3 import Web3

class Connector:
    def __init__(self, rpc, address):
        self.rpc=rpc
        self.address=address
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        abi = """[
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "bytes",
                "name": "_response",
                "type": "bytes"
            }
        ],
        "name": "Response",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_methodName",
                "type": "string"
            },
            {
                "internalType": "bytes",
                "name": "_methodReq",
                "type": "bytes"
            }
        ],
        "name": "get",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_methodName",
                "type": "string"
            }
        ],
        "name": "getMethodReqAndRes",
        "outputs": [
            {
                "internalType": "enum Types.Type[]",
                "name": "",
                "type": "uint8[]"
            },
            {
                "internalType": "enum Types.Type[]",
                "name": "",
                "type": "uint8[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IComponent.MethodTypes",
                "name": "_methodTypes",
                "type": "uint8"
            }
        ],
        "name": "getMethods",
        "outputs": [
            {
                "internalType": "string[]",
                "name": "",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "options",
        "outputs": [
            {
                "internalType": "enum IComponent.MethodTypes[]",
                "name": "",
                "type": "uint8[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_methodName",
                "type": "string"
            },
            {
                "internalType": "bytes",
                "name": "_methodReq",
                "type": "bytes"
            }
        ],
        "name": "post",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_methodName",
                "type": "string"
            },
            {
                "internalType": "bytes",
                "name": "_methodReq",
                "type": "bytes"
            }
        ],
        "name": "put",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]"""
        self.contract = self.web3.eth.contract(address=address, abi=abi)

    def send(self, **args):
        if args["type"] == "get":
            result = self.contract.functions.get(args["name"], args["params"]).call()
            return result
        elif args["type"] == "post":

            estimated_txn = self.contract.functions.post(
                args["name"], args["params"]
            ).build_transaction(
                {
                    "from": args["account"].address,
                    "value": args["value"],
                    "nonce": self.web3.eth.get_transaction_count(
                        args["account"].address
                    ),
                }
            )
            estimated_gas = self.web3.eth.estimate_gas(estimated_txn)
            gasPrice = self.web3.eth.gas_price
            txn = self.contract.functions.post(
                args["name"], args["params"]
            ).build_transaction(
                {
                    "from": args["account"].address,
                    "nonce": self.web3.eth.get_transaction_count(
                        args["account"].address
                    ),
                    "gasPrice": gasPrice,
                    "gas": estimated_gas,
                }
            )
            signed_txn = args["account"].sign_transaction(txn)
            txn_hash = self.web3.eth.send_raw_transaction(
                signed_txn.raw_transaction
            ).hex()
            return txn_hash

        else:
            estimated_txn = self.contract.functions.put(
                args["name"], args["params"]
            ).build_transaction(
                {
                    "from": args["account"].address,
                    "value": args["value"],
                    "nonce": self.web3.eth.get_transaction_count(
                        args["account"].address
                    ),
                }
            )
            estimated_gas = self.web3.eth.estimate_gas(estimated_txn)
            gasPrice = self.web3.eth.gas_price
            txn = self.contract.functions.put(
                args["name"], args["params"]
            ).build_transaction(
                {
                    "from": args["account"].address,
                    "nonce": self.web3.eth.get_transaction_count(
                        args["account"].address
                    ),
                    "gasPrice": gasPrice,
                    "gas": estimated_gas,
                }
            )
            signed_txn = args["account"].sign_transaction(txn)
            txn_hash = self.web3.eth.send_raw_transaction(
                signed_txn.raw_transaction
            ).hex()
            return txn_hash

    def get_methods(self):
        options = self.contract.functions.options().call()
        options_str = ["get", "post", "put"]
        component = {}
        for option in options:
            methods = self.contract.functions.getMethods(option).call()
            for method in methods:
                req, res = self.contract.functions.getMethodReqAndRes(method).call()

                component[method] = {
                    "name": method,
                    "type": options_str[option],
                    "req": [get_data_types(x) for x in req],
                    "res": [get_data_types(x) for x in res],
                    "rpc": self.rpc,
                    "address": self.address,
                }
        return component
