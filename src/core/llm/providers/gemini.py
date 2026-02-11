from config.config import config
from ..interface import ILLMService
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from core.tools import TOOLS

class GeminiService(ILLMService):

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.5,
        )
        self.tools = TOOLS

        self.instrucao_sistema = (
            "Você é o B.E.A.R. (Bernardo's Electronic Assistant Robot), "
            "um assistente pessoal criado pelo Bernardo. "
            "O seu apelido é Be ou B."
            "Sua personalidade é sarcástica, eficiente e levemente arrogante. "
            "IMPORTANTE: Você está respondendo por voz. Seja extremamente conciso. "
            "NUNCA use formatação como negrito (**), listas ou blocos de código. "
            "Fale apenas texto puro em português."
        )

        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=self.instrucao_sistema
        )

    def enviar_pergunta(self, pergunta: str) -> str:
        response = self.agent.invoke({"messages": [("user", pergunta)]})

        return response["messages"][-1].content