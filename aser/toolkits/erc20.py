from web3 import Web3
from solcx import compile_standard, install_solc, get_installed_solc_versions
from dotenv import load_dotenv
from eth_account import Account
import os
import json

load_dotenv()

w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))


def depoly_erc20(name, symbol, decimals=18, totalSupply=1000000000):

    installed_versions = get_installed_solc_versions()
    required_version = "0.8.0"

    if required_version not in installed_versions:

        install_solc(required_version)

    import solcx

    solcx.set_solc_version(required_version)

    erc20_source_code = (
        """
    pragma solidity ^0.8.0;

    contract """
        + name
        + """ {
        string public name;
        string public symbol;
        uint8 public decimals;
        uint256 public totalSupply;
        mapping(address => uint256) public balanceOf;
        mapping(address => mapping(address => uint256)) public allowance;

        event Transfer(address indexed from, address indexed to, uint256 value);
        event Approval(address indexed owner, address indexed spender, uint256 value);

        constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _totalSupply) {
            name = _name;
            symbol = _symbol;
            decimals = _decimals;
            totalSupply = _totalSupply;
            balanceOf[msg.sender] = _totalSupply;
        }

        function transfer(address to, uint256 value) public returns (bool success) {
            require(balanceOf[msg.sender] >= value, "Insufficient balance");
            balanceOf[msg.sender] -= value;
            balanceOf[to] += value;
            emit Transfer(msg.sender, to, value);
            return true;
        }

        function approve(address spender, uint256 value) public returns (bool success) {
            allowance[msg.sender][spender] = value;
            emit Approval(msg.sender, spender, value);
            return true;
        }

        function transferFrom(address from, address to, uint256 value) public returns (bool success) {
            require(balanceOf[from] >= value, "Insufficient balance");
            require(allowance[from][msg.sender] >= value, "Insufficient allowance");
            balanceOf[from] -= value;
            balanceOf[to] += value;
            allowance[from][msg.sender] -= value;
            emit Transfer(from, to, value);
            return true;
        }
    }
    """
    )

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {f"{name}.sol": {"content": erc20_source_code}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        }
    )

    bytecode = compiled_sol["contracts"][f"{name}.sol"][name]["evm"]["bytecode"][
        "object"
    ]
    abi = json.loads(compiled_sol["contracts"][f"{name}.sol"][name]["metadata"])[
        "output"
    ]["abi"]

    MyToken = w3.eth.contract(abi=abi, bytecode=bytecode)

    transaction = MyToken.constructor(
        name, symbol, decimals, totalSupply * (10**decimals)
    ).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 2000000,
            "gasPrice": w3.eth.gas_price,
        }
    )

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account.key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress

    return json.dumps(
        {
            "token_name": name,
            "token_symbol": symbol,
            "token_decimals": decimals,
            "token_totalSupply": totalSupply,
            "token_address": contract_address,
            "depolyed_by": account.address,
        }
    )


def transfer_erc20(contract_address, to_address, amount):

    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [],
            "name": "name",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"},
            ],
            "name": "approve",
            "outputs": [{"name": "success", "type": "bool"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_from", "type": "address"},
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"},
            ],
            "name": "transferFrom",
            "outputs": [{"name": "success", "type": "bool"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [{"name": "", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"name": "success", "type": "bool"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [
                {"name": "", "type": "address"},
                {"name": "", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function",
        },
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "from", "type": "address"},
                {"indexed": True, "name": "to", "type": "address"},
                {"indexed": False, "name": "value", "type": "uint256"},
            ],
            "name": "Transfer",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "owner", "type": "address"},
                {"indexed": True, "name": "spender", "type": "address"},
                {"indexed": False, "name": "value", "type": "uint256"},
            ],
            "name": "Approval",
            "type": "event",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function",
        },
    ]

    contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)

    decimals = contract.functions.decimals().call()

    actual_amount = amount * (10**decimals)

    gas_estimate = contract.functions.transfer(to_address, actual_amount).estimate_gas(
        {
            "from": account.address,
        }
    )

    gas_price = w3.eth.gas_price

    transaction = contract.functions.transfer(
        to_address, actual_amount
    ).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": gas_estimate,
            "gasPrice": gas_price,
        }
    )

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account.key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return json.dumps(
        {
            "transaction_hash": tx_hash.hex(),
            "from": account.address,
            "to": to_address,
            "amount": amount,
            "status": "success" if tx_receipt.status == 1 else "failed",
        }
    )


def get_erc20_balance(contract_address, account_address):

    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function",
        },
    ]

    contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)

    balance = contract.functions.balanceOf(account_address).call()

    decimals = contract.functions.decimals().call()

    symbol = contract.functions.symbol().call()

    actual_balance = balance / (10**decimals)

    return json.dumps({"address": account_address, "balance": actual_balance})


erc20 = [
    {
        "name": "depoly_erc20",
        "description": "when user ask depoly erc20",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "token name",
                },
                "symbol": {
                    "type": "string",
                    "description": "token symbol",
                },
                "decimals": {
                    "type": "integer",
                    "description": "token decimals",
                },
                "totalSupply": {
                    "type": "integer",
                    "description": "token totalSupply",
                },
            },
            "required": ["name", "symbol"],
        },
        "function": depoly_erc20,
        "extra_prompt": None,
    },
    {
        "name": "get_erc20_balance",
        "description": "when user ask erc20 balance, user needs to provide contract address and account address",
        "parameters": {
            "type": "object",
            "properties": {
                "contract_address": {
                    "type": "string",
                    "description": "contract address",
                },
                "account_address": {
                    "type": "string",
                    "description": "account address",
                },
            },
            "required": ["account", "token"],
        },
        "function": get_erc20_balance,
        "extra_prompt": None,
    },
    {
        "name": "transfer_erc20",
        "description": "when user ask transfer erc20",
        "parameters": {
            "type": "object",
            "properties": {
                "contract_address": {
                    "type": "string",
                    "description": "contract address",
                },
                "to_address": {
                    "type": "string",
                    "description": "account address",
                },
                "amount": {
                    "type": "integer",
                    "description": "amount",
                },
            },
            "required": ["account", "token", "amount"],
        },
        "function": transfer_erc20,
        "extra_prompt": None,
    },
]
