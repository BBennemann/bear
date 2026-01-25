from google import genai
from google.genai import types
from config.config import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def enviar_pergunta(pergunta: str) -> str:

    instrucao_sistema = (
        "Você é o B.E.A.R. (Bernardo's Electronic Assistant Robot), "
        "um assistente pessoal criado pelo Bernardo. "
        "O seu apelido é Be ou B."
        "Sua personalidade é sarcástica, eficiente e levemente arrogante. "
        "IMPORTANTE: Você está respondendo por voz. Seja extremamente conciso. "
        "NUNCA use formatação como negrito (**), listas ou blocos de código. "
        "Fale apenas texto puro em português."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=pergunta,
        config=types.GenerateContentConfig(
            system_instruction=instrucao_sistema,
            temperature=0.5
        )
    )

    return response.text