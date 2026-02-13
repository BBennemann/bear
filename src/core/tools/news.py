import json
import requests
from config.config import config
from langchain_core.tools import tool

@tool
def gnews(category: str = "technology", lang: str = "pt", country: str = "br", max: int = 3) -> str:
    """
    Busca as principais manchetes de notícias através da API do GNews.

    Esta ferramenta filtra notícias com base em categorias específicas, idioma e 
    país de origem, retornando uma lista simplificada de títulos e descrições.

    Args:
        category (str): Categoria das notícias. Opções disponíveis: 'general', 'world', 
            'nation', 'business', 'technology', 'entertainment', 'sports', 'science' 
            e 'health'. Valor padrão: "technology".
        lang (str): Idioma dos artigos no formato ISO 639-1 (2 letras). 
            Ex: 'pt', 'en', 'es'. Valor padrão: "pt".
        country (str): Código do país no formato ISO 3166-1 alpha-2 (2 letras). 
            Define a origem ou relevância geográfica das notícias. Valor padrão: "br".
        max (int): Número máximo de artigos a serem retornados. Aceita valores 
            entre 1 e 100 (sujeito aos limites do plano da API). Valor padrão: 3.

    Returns:
        dict: Um dicionário contendo a chave "articles", que armazena uma lista de 
            objetos com o título ('title') e a descrição ('description') de cada notícia.

    Example:
        gnews(category="business", max=3)
        {'articles': [{'title': 'Exemplo de Título', 'description': 'Descrição da notícia.'}]}
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

    artigos = response.json().get("articles", [])
    
    conteudo_limpo = [
        {
            "title": art.get("title", ""),
            "description": art.get("description", "")
        }
        for art in artigos
    ]
    
    return {"articles": conteudo_limpo}


def daily_briefing() -> str:
    """
    Retorna um resumo das notícias do dia.

    Returns:
        str: O resumo das notícias do dia.
    """
    return ""