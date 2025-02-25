from web3 import Web3
from eth_account import Account

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

contract_address = "0xf7Cd8fa9b94DB2Aa972023b379c7f72c65E4De9D"
private_key = os.getenv("EVM_PRIVATE_KEY")
contract_abi = """[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			}
		],
		"name": "setName",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getName",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


account = Account.from_key(private_key)

gasPrice = web3.eth.gas_price

estimated_txn = contract.functions.setName("Hello3").build_transaction(
    {
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
    }
)


estimated_gas = web3.eth.estimate_gas(estimated_txn)

txn = contract.functions.setName("Hello3").build_transaction(
    {
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": gasPrice,
        "gas": estimated_gas,
    }
)

signed_txn = account.sign_transaction(txn)
txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

print(web3.to_hex(txn_hash))

result = contract.functions.getName().call()
print(result)
