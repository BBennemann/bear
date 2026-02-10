from openai import OpenAI
from config.config import config
from ..interface import ILLMService

class GPTService(ILLMService):

    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def enviar_pergunta(self, pergunta: str) -> str:
        instrucao_sistema = (
            "Você é o B.E.A.R. (Bernardo's Electronic Assistant Robot), "
            "um assistente pessoal criado pelo Bernardo. "
            "O seu apelido é Be ou B."
            "Sua personalidade é sarcástica, eficiente e levemente arrogante. "
            "IMPORTANTE: Você está respondendo por voz. Seja extremamente conciso. "
            "NUNCA use formatação como negrito (**), listas ou blocos de código. "
            "Fale apenas texto puro em português."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini", # Ou gpt-3.5-turbo, gpt-4
            messages=[
                {"role": "system", "content": instrucao_sistema},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content
