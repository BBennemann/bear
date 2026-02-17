import json
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.config.config import config
from langchain_core.tools import tool

@tool
def weather_data(city_name: str = "florianopolis", days: int = 2):
    """
    Obtém a previsão do tempo para uma cidade.

    Args:
        city_name (str): Nome da cidade. Valor padrão: "florianopolis".
        days (int): Número de dias para a previsão.
            1 = Previsão de hoje.
            2 = Previsão de hoje e amanhã.
            Valor máximo: 2. Valor padrão: 2.
    """
    weather_base_url = f"http://api.weatherapi.com/v1/forecast.json"

    days = min(days, 2)

    params = {
        "key": config.WEATHER_API_KEY,
        "q": city_name,
        "days": days
    }

    response = requests.get(weather_base_url, params)

    response = {
        "city_name": response.json().get("location").get("name"),
        "region_name": response.json().get("location").get("region"),
        "country_name": response.json().get("location").get("country"),
        "previsao": [
            {
                "dia": day.get("date"),
                "temp_max": day.get("day").get("maxtemp_c"),
                "temp_min": day.get("day").get("mintemp_c"),
                "chance_of_rain": day.get("day").get("daily_chance_of_rain"),
                "condicao": day.get("day").get("condition").get("text")
            }
            for day in response.json().get("forecast").get("forecastday")
        ]
    }

    return response


if __name__ == "__main__":
    print(weather_data.invoke({}))
    