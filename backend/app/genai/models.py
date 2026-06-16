import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

QWEN_MODEL = "qwen2.5"
GPT_FIVE_MODEL = "gpt-5"
GPT_FIVE_MINI_MODEL = "gpt-5-mini"
API_KEY_ENV_VAR_NAME = "GENAI_API_KEY"
API_URL_ENV_VAR_NAME = "GENAI_URL_BASE"
API_VERSION = "2023-05-15"
API_KEY_HEADER = "X-API-KEY"

load_dotenv(override=True)

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

def get_gpt_five_mini() -> AzureChatOpenAI:
    api_key = os.getenv(API_KEY_ENV_VAR_NAME)
    api_base_url = os.getenv(API_URL_ENV_VAR_NAME)

    return AzureChatOpenAI(
        api_key=api_key,
        api_version=API_VERSION,
        default_headers={API_KEY_HEADER: api_key},
        temperature=0,
        base_url= api_base_url + GPT_FIVE_MINI_MODEL,
        model=GPT_FIVE_MINI_MODEL,
    )

def get_gemini() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GEMINI_API_KEY")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0,
    )
