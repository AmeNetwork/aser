import requests
import json

chains = {
    "ETHEREUM": "1",
    "BSC": "56",
    "ARBITRUM": "42161",
    "POLYGON": "137",
    "ZKSYNC ERA": "324",
    "LINEA MAINNET": "59144",
    "BASE": "8453",
    "SCROLL": "534352",
    "OPTIMISM": "10",
    "AVALANCHE": "43114",
    "FANTOM": "250",
    "CRONOS": "25",
    "OKC": "66",
    "HECO": "128",
    "GNOSIS": "100",
    "ETHW": "10001",
    "TRON": "tron",
    "KCC": "321",
    "FON": "201022",
    "MANTLE": "5000",
    "OPBNB": "204",
    "ZKFAIR": "42766",
    "BLAST": "81457",
    "MANTA PACIFIC": "169",
    "BERACHAIN": "80094",
    "ABSTRACT": "2741",
    "HASHKEY CHAIN": "177",
    "SONIC": "146",
    "STORY": "1514",
}


def convert_to_yes_no(value):
    if value == "0":
        return "NO"
    elif value == "1":
        return "YES"
    else:
        return str(value)


def check_contract(chain_name, contract_address):
    chain_id = chains.get(chain_name.upper())

    base_url = "https://api.gopluslabs.io/api/v1/token_security"
    url = f"{base_url}/{chain_id}"

    params = {"contract_addresses": contract_address}

    headers = {"accept": "*/*"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:

        if response.json()["message"]=="OK":

            response_json = response.json()["result"][contract_address]

            def get_value(key):
                return response_json.get(key, "unknown")

            return_str = f"""
            Token Address: {contract_address}
            Token Name: {get_value("token_name")}
            Token Symbol: {get_value("token_symbol")}
            Token Total Supply: {get_value("total_supply")}
            Holder Count: {get_value("holder_count")}
            Creator Address: {get_value("creator_address")}
            Creator Balance: {get_value("creator_balance")}
            Buy Tax: {convert_to_yes_no(get_value("buy_tax"))}
            Sell Tax: {convert_to_yes_no(get_value("sell_tax"))}
            Transfer Pausable: {convert_to_yes_no(get_value("transfer_pausable"))}
            Can't Buy: {convert_to_yes_no(get_value("cannot_buy"))}
            Can't Sell All: {convert_to_yes_no(get_value("cannot_sell_all"))}
            Hidden Owner: {convert_to_yes_no(get_value("hidden_owner"))}
            Blacklist: {convert_to_yes_no(get_value("is_blacklisted"))}
            Whitelist: {convert_to_yes_no(get_value("is_whitelisted"))}
            Honeypot: {convert_to_yes_no(get_value("is_honeypot"))}
            Open Source: {convert_to_yes_no(get_value("is_open_source"))}

            """

           
        else:
            return_str = f"""
            {response.json()["message"]}
            """
        return return_str
    else:
        chain_names = list(chains.keys())
        chain_names_string = ",".join(chain_names)
        return_str = f"""
        Supported Chains: {chain_names_string}
        Example:Ethereum 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48  
        """
        return {"error": "Failed to retrieve data", "message": f""}


# chain_name = "Ethereum"
# contract_address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

# result=check_contract(chain_name, contract_address)
# print(result)

goplus = [
    {
        "name": "check_contract",
        "description": "get contract info by chain name and contract address",
        "parameters": {
            "type": "object",
            "properties": {
                "chain_name": {
                    "type": "string",
                    "description": "chain name",
                },
                "contract_address": {
                    "type": "string",
                    "description": "contract address",
                },
            },
            "required": ["chain_name", "contract_address"],
        },
        "function": check_contract,
        "extra_prompt": None,
        "example": "Ethereum 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    }
]
