from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def create_llm_client():
    return OpenAI(
        base_url = os.getenv("OLLAMA_BASE_URL"),
        api_key = "ollama"
    )