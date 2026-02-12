from config.config import config
from .base import BaseLLMAgent 
from langchain_openai import ChatOpenAI

class GPTService(BaseLLMAgent): 

    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=config.OPENAI_API_KEY,
            temperature=0.5
        )
        
        super().__init__(model)


