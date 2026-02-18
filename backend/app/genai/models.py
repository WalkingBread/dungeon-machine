from langchain_openai import AzureChatOpenAI
# from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

QWEN_MODEL = "qwen2.5"
GPT_FIVE_MODEL = "gpt-5"
API_KEY_ENV_VAR_NAME = "GENAI_API_KEY"
API_URL_ENV_VAR_NAME = "GENAI_URL_BASE"
API_VERSION = "2023-05-15"
API_KEY_HEADER = "X-API-KEY"

load_dotenv(override=True)

# def get_qwen(ctx_window: int) -> ChatOllama:
#     return ChatOllama(
#         model=QWEN_MODEL,
#         num_ctx=ctx_window,
#         temperature=0
#     )

def get_gpt_five() -> AzureChatOpenAI:
    api_key = os.getenv(API_KEY_ENV_VAR_NAME)
    api_base_url = os.getenv(API_URL_ENV_VAR_NAME)

    return AzureChatOpenAI(
        api_key=api_key,
        api_version=API_VERSION,
        default_headers={API_KEY_HEADER: api_key},
        temperature=0,
        base_url= api_base_url + GPT_FIVE_MODEL,
        model=GPT_FIVE_MODEL,
    )