import requests
import os
from dotenv import load_dotenv

load_dotenv()
def get_cryptocurrency_price(symbol):

    symbol_upper=symbol.upper()

    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv("COINMARKETCAP_API_KEY"),
    }
    
    parameters = {
        'symbol':symbol_upper,
        'convert': 'USD',
        'aux':'circulating_supply'
    }


    
    try:

        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  
        data = response.json()
        
        price = data['data'][symbol_upper][0]['quote']['USD']['price']

        return f"The current price of {symbol} is: ${price:.2f}"

    except :
        return "Not Found"

# price=get_cryptocurrency_price("bnb")
# print(price)

coinmarketcap = [
    {
        "name": "get_cryptocurrency_price",
        "description": "This function is used to fetch real-time cryptocurrency prices. Use it when asked about current prices or market values of cryptocurrencies. Get the current price of a cryptocurrency by its token symbol. Supports major cryptocurrencies like BTC, ETH, USDT, etc.", 
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The cryptocurrency token symbol (e.g., BTC for Bitcoin, ETH for Ethereum)",
                }
            },
            "required": ["symbol"],
        },
        "function": get_cryptocurrency_price,
        "extra_prompt": None,
        "example":"get price of bitcoin, btc price"
    }
]
