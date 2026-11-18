import json
import requests
import sys
import os
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.config.config import config
from langchain_core.tools import tool

@tool
def get_news(category: str = "general", lang: str = "en", country: str = "us", max: Optional[int] = 3) -> dict:
    """
    Fetches top news headlines using the GNews API.
    
    Use this tool when the user asks for today's news, latest updates on a general topic, or what's happening in the world or country.

    Args:
        category (str): News category. Options: 'general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health'. Default: "technology".
        lang (str): Language of the articles (ISO 639-1, 2 letters). Ex: 'en', 'es', 'pt'. Try to guess from the user's request. Default: "en".
        country (str): Country (ISO 3166-1 alpha-2, 2 letters). Ex: 'us', 'gb', 'br'. Default: "us".
        max (int, optional): Maximum number of articles to return. Default: 3.

    Returns:
        dict: A dictionary containing the list of news articles (title and description).
    """
    gnews_base_url = "https://gnews.io/api/v4/top-headlines?"

    params = {
        "category": category,
        "lang": lang,
        "country": country,
        "max": max,
        "apikey": config.GNEWS_API_KEY
    }

    for k, v in params.items():
        gnews_base_url += f"{k}={v}&"

    response = requests.get(gnews_base_url)

    articles = response.json().get("articles", [])
    
    clean_content = [
        {
            "title": art.get("title", ""),
            "description": art.get("description", "")
        }
        for art in articles
    ]
    
    return {"articles": clean_content}

if __name__ == "__main__":
    print(get_news.invoke({}))