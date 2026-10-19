from openai import OpenAI


def create_llm_client():
    return OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key = "ollama"
    )