from .jokes import joke
from .news import get_news
from .money_exchange import exchange_rates
from .weather import get_weather_data

TOOLS = [joke, get_news, exchange_rates, get_weather_data]