from langchain_google_genai import ChatGoogleGenerativeAI
from .config import settings 

settings.GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.2,
)

print(f"LLM ({llm.model}) instanciado en llm_setup.py.")