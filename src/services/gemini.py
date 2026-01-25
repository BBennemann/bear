from google import genai

client = genai.Client()

def enviar_pergunta(pergunta: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=pergunta,
    )

    return response.text