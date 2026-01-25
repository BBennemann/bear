from google import genai
from config.config import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def enviar_pergunta(pergunta: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=pergunta,
    )

    return response.text