from config.config import config
from .base import BaseLLMAgent 
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiService(BaseLLMAgent): 

    def __init__(self):
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.5,
        )
        
        super().__init__(model)