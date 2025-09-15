import requests
import os
from dotenv import load_dotenv
from aser.tools import tool
@tool()
def coinmarketcap(symbol:str):
    """
    get cryptocurrency price
    """
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



 