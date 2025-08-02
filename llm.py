from langchain_groq import ChatGroq
import os

def get_llm():
    return ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY")
    )
