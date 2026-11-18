import json
import requests
import sys
import os
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.config.config import config
from langchain_core.tools import tool

@tool
def exchange_rates(base_coin: str = "EUR", target_coin: str = "BRL", amount: Optional[str] = None):
    """
    Gets the exchange rate and converts values between two currencies.
    
    Use this tool when the user asks for the value of one currency against another (e.g., "How much is a dollar?", "Convert 50 euros to dollars"). It is mandatory to use 3-letter ISO 4217 codes.

    Args:
        base_coin (str): Base/source currency code (e.g., "USD", "EUR", "GBP"). Default: "USD".
        target_coin (str): Target/destination currency code (e.g., "EUR", "USD"). Default: "EUR".
        amount (str, optional): Amount to be converted (e.g., "50", "15.5"). If omitted, returns only the rate for 1 unit.

    Returns:
        dict: Dictionary containing currency codes, updated conversion rate, and total converted value.
    """
    exchange_rates_url = f"https://v6.exchangerate-api.com/v6/{config.EXCHANGERATE_API_KEY}/pair/{base_coin}/{target_coin}"

    if amount:
        exchange_rates_url += f"/{amount}"

    response = requests.get(exchange_rates_url)

    response_data = {
        "base_code": response.json().get("base_code"),
        "target_code": response.json().get("target_code"),
        "conversion_rate": response.json().get("conversion_rate"),
        "amount": response.json().get("conversion_result")
    }

    return {"response": response_data}

if __name__ == "__main__":
    print(exchange_rates.invoke({}))