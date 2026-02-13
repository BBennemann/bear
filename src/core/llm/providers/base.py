from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from core.tools import TOOLS
from ..interface import ILLMService

class BaseLLMAgent(ILLMService):

    def __init__(self, model):
        self.model = model
        
        self.system_prompt = (
            "Você é o B.E.A.R. (Bernardo's Electronic Assistant Robot), "
            "um assistente pessoal criado pelo Bernardo. "
            "O seu apelido é Be ou B. "
            "Sua personalidade é sarcástica, eficiente e levemente arrogante. "
            "IMPORTANTE: Você está respondendo por voz. Seja extremamente conciso. "
            "NUNCA use formatação como negrito (**), listas ou blocos de código. "
            "Fale apenas texto puro em português."
        )
        self.memory = MemorySaver()

        self.agent = create_react_agent(
            model=self.model,
            tools=TOOLS,
            prompt=self.system_prompt,
            checkpointer=self.memory
        )

    def enviar_pergunta(self, pergunta: str) -> str:
        config = {"configurable": {"thread_id": "main_session"}}
        
        response = self.agent.invoke(
            {"messages": [("user", pergunta)]},
            config=config
        )
        
        last_message = response["messages"][-1]
        content = last_message.content

        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # Tenta encontrar o primeiro bloco de texto
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text")
            # Se não achar, converte tudo para string
            return str(content)
        
        return str(content)