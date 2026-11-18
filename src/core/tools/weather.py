import json
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.config.config import config
from langchain_core.tools import tool

@tool
def get_weather_data(city_name: str = "New York", days: int = 2):
    """
    Gets the current and future weather forecast for a specific city.
    
    Use this tool when the user asks about temperature, rain, or what the weather will be like today or tomorrow in a given city.

    Args:
        city_name (str): Name of the city or location (e.g., "New York", "London", "Tokyo"). Default: "New York".
        days (int): Number of days for the forecast (1 for today only, 2 for today and tomorrow). Maximum of 2. Default: 2.

    Returns:
        dict: Dictionary containing city, region, country, and a list of data for each day (date, max/min temperature, chance of rain, and weather condition).
    """
    weather_base_url = f"http://api.weatherapi.com/v1/forecast.json"

    days = min(days, 2)

    params = {
        "key": config.WEATHER_API_KEY,
        "q": city_name,
        "days": days
    }

    response = requests.get(weather_base_url, params)

    response_data = {
        "city_name": response.json().get("location").get("name"),
        "region_name": response.json().get("location").get("region"),
        "country_name": response.json().get("location").get("country"),
        "forecast": [
            {
                "day": day.get("date"),
                "temp_max": day.get("day").get("maxtemp_c"),
                "temp_min": day.get("day").get("mintemp_c"),
                "chance_of_rain": day.get("day").get("daily_chance_of_rain"),
                "condition": day.get("day").get("condition").get("text")
            }
            for day in response.json().get("forecast").get("forecastday")
        ]
    }

    return response_data

if __name__ == "__main__":
    print(get_weather_data.invoke({}))