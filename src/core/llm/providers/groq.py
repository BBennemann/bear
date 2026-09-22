from config.config import config
from .base import BaseLLMAgent 
from groq import Groq
from langchain_groq import ChatGroq

class GroqService(BaseLLMAgent): 

    def __init__(self):
        model = ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=config.GROQ_API_KEY,
            temperature=0.5
        )
        
        super().__init__(model)


