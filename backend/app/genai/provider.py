import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv
from enum import Enum

load_dotenv(override=True)

API_KEY_ENV_VAR_NAME = "GENAI_API_KEY"
API_URL_ENV_VAR_NAME = "GENAI_URL_BASE"
API_VERSION = "2023-05-15"
API_KEY_HEADER = "X-API-KEY"

class Model(str, Enum):
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"

    def __str__(self) -> str:
        return self.value

class ModelProvider:
    def __init__(self):
        self.available_models = {
            Model.GPT_5: lambda: self._get_azure_model(Model.GPT_5),
            Model.GPT_5_MINI: lambda: self._get_azure_model(Model.GPT_5_MINI),
        }

    def get_model(self, model: Model):
        return self.available_models[model]()

    def _get_azure_model(self, model_name):
        api_key = os.getenv(API_KEY_ENV_VAR_NAME)
        api_base_url = os.getenv(API_URL_ENV_VAR_NAME)

        return AzureChatOpenAI(
            api_key=api_key,
            api_version=API_VERSION,
            default_headers={API_KEY_HEADER: api_key},
            temperature=0,
            base_url= api_base_url + model_name,
            model=model_name,
        )