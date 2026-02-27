from langchain_openai import AzureChatOpenAI, OpenAIEmbeddings
# from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
from pydantic import SecretStr
from requests.utils import default_headers
from langchain_huggingface import HuggingFaceEmbeddings

QWEN_MODEL = "qwen2.5"
GPT_FIVE_MODEL = "gpt-5"
GPT_FIVE_MINI_MODEL = "gpt-5-mini"
API_KEY_ENV_VAR_NAME = "GENAI_API_KEY"
API_URL_ENV_VAR_NAME = "GENAI_URL_BASE"
API_VERSION = "2023-05-15"
API_KEY_HEADER = "X-API-KEY"

GPT_EMBEDDING_MODEL = "text-embedding-3-large"

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

def get_gpt_embedding() -> OpenAIEmbeddings:
    api_key = os.getenv(API_KEY_ENV_VAR_NAME)
    api_base_url = os.getenv(API_URL_ENV_VAR_NAME)

    if api_key is None or api_base_url is None:
        raise EnvironmentError("Missing api key or api base url in this environment")
    
    return OpenAIEmbeddings(
        api_key=SecretStr(api_key), 
        api_version=API_VERSION, default_headers={API_KEY_HEADER: api_key},
        base_url=api_base_url,
        model=GPT_EMBEDDING_MODEL
    )

def get_hg_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
