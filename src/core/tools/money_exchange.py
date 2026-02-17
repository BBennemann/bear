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
    Obtém a taxa de câmbio entre duas moedas.
    Utilize códigos de moeda ISO 4217 de três letras (ex: USD para Dólares Americanos, EUR para Euro, BRL para Real).
    Caso forneça uma quantidade (amount) em formato decimal (xxxx.xxxx), o cálculo da conversão será feito automaticamente.

    Args:
        base_coin (str): Moeda base (ex: "BRL", "USD", "EUR"). Valor padrão: "EUR".
        target_coin (str): Moeda alvo (ex: "USD", "EUR", "BRL"). Valor padrão: "BRL".
        amount (str, optional): Quantidade a ser convertida. Se não informado, retorna apenas a taxa.

    Returns:
        dict: Resultado da conversão em JSON.
    """
    exchange_rates_url = f"https://v6.exchangerate-api.com/v6/{config.EXCHANGERATE_API_KEY}/pair/{base_coin}/{target_coin}"

    if amount:
        exchange_rates_url += f"/{amount}"

    response = requests.get(exchange_rates_url)

    response = {
        "base_code": response.json().get("base_code"),
        "target_code": response.json().get("target_code"),
        "conversion_rate": response.json().get("conversion_rate"),
        "amount": response.json().get("conversion_result")
    }

    return {"response": response}
    

if __name__ == "__main__":
    print(exchange_rates.invoke({}))