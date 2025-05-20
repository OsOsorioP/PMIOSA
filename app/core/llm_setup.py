from langchain_google_genai import ChatGoogleGenerativeAI
from .config import settings 

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.2,
)

print(f"LLM ({llm.model}) instanciado en llm_setup.py.")