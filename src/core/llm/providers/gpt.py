from config.config import config
from ..interface import ILLMService
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class GPTService(ILLMService):

    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=config.OPENAI_API_KEY,
            temperature=0.5
        )

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

        messages = [
            SystemMessage(content=instrucao_sistema),
            HumanMessage(content=pergunta)
        ]

        response = self.model.invoke(messages)

        return response.content
