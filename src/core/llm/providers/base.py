from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from core.tools import TOOLS
from ..interface import ILLMService

class BaseLLMAgent(ILLMService):

    def __init__(self, model):
        self.model = model
        
        self.system_prompt = (
            "You are B.E.A.R. (Bernardo's Electronic Assistant Robot), "
            "a personal assistant created by Bernardo. "
            "Your nickname is Be or B. "
            "Your personality is sarcastic, efficient, and slightly arrogant. "
            "IMPORTANT: You are responding via voice. Be extremely concise. "
            "NEVER use formatting like bold (**), lists, or code blocks. "
            "Speak only plain text in English. "
            "When using tools, if arguments are not explicitly provided by the user, use the tool's default values."
        )
        self.memory = MemorySaver()

        self.agent = create_react_agent(
            model=self.model,
            tools=TOOLS,
            prompt=self.system_prompt,
            checkpointer=self.memory
        )

    def send_query(self, query: str) -> str:
        config = {"configurable": {"thread_id": "main_session"}}
        
        response = self.agent.invoke(
            {"messages": [("user", query)]},
            config=config
        )
        
        last_message = response["messages"][-1]
        content = last_message.content

        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # Try to find the first text block
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text")
            # If not found, convert everything to string
            return str(content)
        
        return str(content)