from langchain_core.tools import tool
import random

@tool
def piada() -> str:
    """
    Retorna uma piada aleatória.

    Returns:
        str: A piada aleatória.
    """

    jokes_list = [
        "Por que os fantasmas são péssimos para contar mentiras?... Porque são transparentes.",
        "Por que a plantinha não foi atendida no hospital?... Porque só tinha médico de plantão."
    ]
    return random.choice(jokes_list)

def daily_briefing() -> str:
    """
    Retorna um resumo das notícias do dia.

    Returns:
        str: O resumo das notícias do dia.
    """
    return ""
    