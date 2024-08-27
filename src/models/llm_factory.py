from typing import Any, Dict, List, Type

import instructor
from anthropic import AsyncAnthropic
from config.settings import get_settings
from openai import AsyncAzureOpenAI, AsyncOpenAI
from pydantic import BaseModel


class LLMFactory:
    def __init__(self, provider: str = None):
        self.provider = provider if provider is not None else "openai"
        self.settings = getattr(get_settings(), provider)
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        client_initializers = {
            "openai": lambda s: instructor.from_openai(AsyncOpenAI(api_key=s.api_key)),
            "azure_openai": lambda s: instructor.from_openai(AsyncAzureOpenAI(api_key=s.api_key, azure_endpoint=s.azure_endpoint, api_version=s.api_version)),
            "anthropic": lambda s: instructor.from_anthropic(
                AsyncAnthropic(api_key=s.api_key)
            ),
            "llama": lambda s: instructor.from_openai(
                AsyncOpenAI(base_url=s.base_url, api_key=s.api_key),
                mode=instructor.Mode.JSON,
            ),
        }

        initializer = client_initializers.get(self.provider)
        if initializer:
            return initializer(self.settings)
        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        completion_params = {
            "model": kwargs.get("model", self.settings.default_model),
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "response_model": response_model,
            "messages": messages,
        }
        return self.client.chat.completions.create(**completion_params)