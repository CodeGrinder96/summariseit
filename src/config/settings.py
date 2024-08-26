import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class LLMProviderSettings(BaseSettings):
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class OpenAISettings(LLMProviderSettings):
    api_key: str = os.getenv("OPENAI_API_KEY")
    default_model: str = "gpt-4o"


class AzureOpenAISettings(LLMProviderSettings):
    api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version: str = os.getenv("AZURE_OPENAI_API_VERSION")
    default_model: str = "gpt-4o"
    
    
class AnthropicSettings(LLMProviderSettings):
    api_key: str = os.getenv("ANTHROPIC_API_KEY")
    default_model: str = "claude-3-5-sonnet-20240620"
    max_tokens: int = 1024


class LlamaSettings(LLMProviderSettings):
    api_key: str = "key"  # required, but not used
    default_model: str = "llama3"
    base_url: str = "http://localhost:11434/v1"


class Settings(BaseSettings):
    app_name: str = "GenAI Project Template"
    openai: OpenAISettings = OpenAISettings()
    azure_openai: AzureOpenAISettings = AzureOpenAISettings()
    anthropic: AnthropicSettings = AnthropicSettings()
    llama: LlamaSettings = LlamaSettings()


@lru_cache
def get_settings():
    return Settings()