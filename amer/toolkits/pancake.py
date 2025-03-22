from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware


from dotenv import load_dotenv
from eth_account import Account
import os
import json

load_dotenv()

bsc = "https://bsc-dataseed.binance.org/"
bsc_scan = "https://bscscan.com/tx/"
WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
tokens = {
    "bnb": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    "usdt": "0x55d398326f99059fF775485246999027B3197955",
    "cake": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
}


web3 = Web3(Web3.HTTPProvider(bsc))
web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)


account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
pancakeswap_router = "0x10ED43C718714eb63d5aA57B78B54704E256024E"


router_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
        ],
        "name": "getAmountsOut",
        "outputs": [
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        ],
        "name": "swapExactETHForTokens",
        "outputs": [
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        ],
        "name": "swapExactTokensForETH",
        "outputs": [
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


erc20_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
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
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
]


router_contract = web3.eth.contract(address=pancakeswap_router, abi=router_abi)


def get_min_amount_out(amount_in, path, slippage_percentage=0.5):
    amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
    expected_amount_out = amounts_out[-1]
    min_amount_out = int(expected_amount_out * (1 - slippage_percentage / 100))
    return min_amount_out, expected_amount_out


def get_token_decimals(token_address):
    token_contract = web3.eth.contract(address=token_address, abi=erc20_abi)
    return token_contract.functions.decimals().call()


def approve_token(token_address, amount):
    token_contract = web3.eth.contract(address=token_address, abi=erc20_abi)
    approve_txn = token_contract.functions.approve(
        pancakeswap_router, amount
    ).build_transaction(
        {
            "from": account.address,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        }
    )

    gas_estimate = web3.eth.estimate_gas(approve_txn)
    approve_txn["gas"] = int(gas_estimate * 1.2)

    signed_approve_txn = web3.eth.account.sign_transaction(approve_txn, account.key)
    approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_txn.raw_transaction)
    approve_receipt = web3.eth.wait_for_transaction_receipt(approve_tx_hash)


def swap_eth_for_tokens(to_token, amount, slippage_percentage=0.5):
    amount_in_wei = web3.to_wei(amount, "ether")

    wbnb_address = Web3.to_checksum_address(WBNB)
    to_token_address = Web3.to_checksum_address(to_token)

    path = [wbnb_address, to_token_address]

    min_amount_out, expected_amount_out = get_min_amount_out(
        amount_in_wei, path, slippage_percentage
    )

    swap_txn = router_contract.functions.swapExactETHForTokens(
        min_amount_out,
        path,
        account.address,
        web3.eth.get_block("latest")["timestamp"] + 1000,
    ).build_transaction(
        {
            "from": account.address,
            "value": amount_in_wei,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        }
    )

    gas_estimate = web3.eth.estimate_gas(swap_txn)
    swap_txn["gas"] = int(gas_estimate * 1.2)

    signed_swap_txn = web3.eth.account.sign_transaction(swap_txn, account.key)
    swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.raw_transaction)
    return web3.eth.wait_for_transaction_receipt(swap_tx_hash)


def swap_tokens_for_eth(from_token, amount, slippage_percentage=0.5):

    from_token = Web3.to_checksum_address(from_token)

    from_token_decimals = get_token_decimals(from_token)

    amount_in_wei = int(amount * (10**from_token_decimals))

    token_contract = web3.eth.contract(address=from_token, abi=erc20_abi)

    current_allowance = token_contract.functions.allowance(
        account.address, pancakeswap_router
    ).call()

    if current_allowance < amount_in_wei:

        approve_txn = token_contract.functions.approve(
            pancakeswap_router, amount_in_wei
        ).build_transaction(
            {
                "from": account.address,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        gas_estimate = web3.eth.estimate_gas(approve_txn)
        approve_txn["gas"] = int(gas_estimate * 1.2)

        signed_approve_txn = web3.eth.account.sign_transaction(approve_txn, account.key)
        approve_tx_hash = web3.eth.send_raw_transaction(
            signed_approve_txn.raw_transaction
        )
        approve_receipt = web3.eth.wait_for_transaction_receipt(approve_tx_hash)

    path = [from_token, WBNB]
    min_amount_out, expected_amount_out = get_min_amount_out(
        amount_in_wei, path, slippage_percentage
    )

    swap_txn = router_contract.functions.swapExactTokensForETH(
        amount_in_wei,
        min_amount_out,
        path,
        account.address,
        web3.eth.get_block("latest")["timestamp"] + 1000,
    ).build_transaction(
        {
            "from": account.address,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        }
    )

    gas_estimate = web3.eth.estimate_gas(swap_txn)
    swap_txn["gas"] = int(gas_estimate * 1.2)

    signed_swap_txn = web3.eth.account.sign_transaction(swap_txn, account.key)
    swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.raw_transaction)

    swap_receipt = web3.eth.wait_for_transaction_receipt(swap_tx_hash)

    return swap_receipt


def swap_tokens_for_tokens(from_token, to_token, amount, slippage_percentage=0.5):

    from_token = Web3.to_checksum_address(from_token)
    to_token = Web3.to_checksum_address(to_token)

    from_token_decimals = get_token_decimals(from_token)
    to_token_decimals = get_token_decimals(to_token)

    amount_in_wei = int(amount * (10**from_token_decimals))

    token_contract = web3.eth.contract(address=from_token, abi=erc20_abi)

    current_allowance = token_contract.functions.allowance(
        account.address, pancakeswap_router
    ).call()

    if current_allowance < amount_in_wei:

        approve_txn = token_contract.functions.approve(
            pancakeswap_router, amount_in_wei
        ).build_transaction(
            {
                "from": account.address,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        gas_estimate = web3.eth.estimate_gas(approve_txn)
        approve_txn["gas"] = int(gas_estimate * 1.2)

        signed_approve_txn = web3.eth.account.sign_transaction(approve_txn, account.key)
        approve_tx_hash = web3.eth.send_raw_transaction(
            signed_approve_txn.raw_transaction
        )
        approve_receipt = web3.eth.wait_for_transaction_receipt(approve_tx_hash)

    path = [from_token, to_token]
    min_amount_out, expected_amount_out = get_min_amount_out(
        amount_in_wei, path, slippage_percentage
    )

    swap_txn = router_contract.functions.swapExactTokensForTokens(
        amount_in_wei,
        min_amount_out,
        path,
        account.address,
        web3.eth.get_block("latest")["timestamp"] + 1000,
    ).build_transaction(
        {
            "from": account.address,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        }
    )

    gas_estimate = web3.eth.estimate_gas(swap_txn)
    swap_txn["gas"] = int(gas_estimate * 1.2)

    signed_swap_txn = web3.eth.account.sign_transaction(swap_txn, account.key)
    swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.raw_transaction)

    swap_receipt = web3.eth.wait_for_transaction_receipt(swap_tx_hash)

    return swap_receipt


def check_balance(from_token, amount):

    token_address = Web3.to_checksum_address(from_token)

    if token_address.lower() == WBNB.lower():

        balance = web3.eth.get_balance(account.address)
        balance_in_ether = web3.from_wei(balance, "ether")
        if balance_in_ether < amount:
            return False
    else:

        token_contract = web3.eth.contract(address=token_address, abi=erc20_abi)
        balance = token_contract.functions.balanceOf(account.address).call()
        decimals = token_contract.functions.decimals().call()
        balance_in_token = balance / (10**decimals)
        if balance_in_token < amount:
            return False

    return True


def get_balance(token_symbol):

    from_token_name = token_symbol.lower()

    supported_tokens = list(tokens.keys())

    if from_token_name not in supported_tokens:
        missing_token = (
            from_token_name if from_token not in supported_tokens else to_token_name
        )
        return f"{missing_token} is not supported. Supported tokens are: {', '.join(supported_tokens)}"
    else:
        from_token_address = Web3.to_checksum_address(tokens[from_token_name])

        if from_token_address.lower() == WBNB.lower():
            balance = web3.eth.get_balance(account.address)
            balance_in_ether = web3.from_wei(balance, "ether")
            return  json.dumps({"balance": str(balance_in_ether),"token_address": WBNB})
        else:
            token_contract = web3.eth.contract(
                address=from_token_address, abi=erc20_abi
            )
            balance = token_contract.functions.balanceOf(account.address).call()
            decimals = token_contract.functions.decimals().call()
            balance_in_token = balance / (10**decimals)
            return json.dumps({"balance": balance_in_token,"token_address": from_token_address})



def swap(from_token, to_token, amount, slippage_percentage=0.5):

    try:
        from_token_name = from_token.lower()
        to_token_name = to_token.lower()

        supported_tokens = list(tokens.keys())

        if (
            from_token_name not in supported_tokens
            or to_token_name not in supported_tokens
        ):
            missing_token = (
                from_token_name if from_token not in supported_tokens else to_token_name
            )
            return f"{missing_token} is not supported. Supported tokens are: {', '.join(supported_tokens)}"

        from_token_address = tokens[from_token_name]
        to_token_address = tokens[to_token_name]

        if from_token_address.lower() == to_token_address.lower():
            return "The from_token and to_token cannot be the same."

        if not check_balance(from_token_address, amount):
            return f"Insufficient balance for {from_token}."

        result = ""
        if from_token_address.lower() == WBNB.lower():

            result = swap_eth_for_tokens(to_token_address, amount, slippage_percentage)
        elif to_token_address.lower() == WBNB.lower():

            result = swap_tokens_for_eth(
                from_token_address, amount, slippage_percentage
            )
        else:

            result = swap_tokens_for_tokens(
                from_token_address, to_token_address, amount, slippage_percentage
            )
        return json.dumps(
            {
                "account": account.address,
                "from_token_name": from_token,
                "from_token_address": from_token_address,
                "to_token_name": to_token,
                "to_token_address": to_token_address,
                "amount": amount,
                "slippage_percentage": f"{slippage_percentage}%",
                "result": f"{bsc_scan}0x{result['transactionHash'].hex()}",
            }
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback

        traceback.print_exc()

    # result = swap("BNB", "usdt", 0.0000001)

    # print(result)


pancake = [
    {
        "name": "swap",
        "description": "Swap or exchange tokens on PancakeSwap and return detailed transaction information, It will return a json format string.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_token": {
                    "type": "string",
                    "description": "from token symbol",
                },
                "to_token": {
                    "type": "string",
                    "description": "to token symbol",
                },
                "amount": {
                    "type": "number",
                    "description": "exchange amount",
                },
                "slippage_percentage": {
                    "type": "number",
                    "description": "slippage percentage",
                },
            },
            "required": ["from_token", "to_token", "amount"],
        },
        "function": swap,
        "extra_prompt": "show more information, including account address, from_token address, to_token address, amount, slippage_percentage, result",
        "example":"exchange 0.01 bnb to usdt"
    }, {
        "name": "get_balance",
        "description": "get token balance by token symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "token_symbol": {
                    "type": "string",
                    "description": "token symbol",
                }
            },
            "required": ["token_symbol"],
        },
        "function": get_balance,
        "extra_prompt": "you must show more information, including balance, token_address",
        "example":"get my bnb balance"
    }
]
