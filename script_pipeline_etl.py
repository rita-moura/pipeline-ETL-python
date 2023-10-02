import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise EnvironmentError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo config.env.")

