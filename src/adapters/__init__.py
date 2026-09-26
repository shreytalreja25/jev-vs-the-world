"""
Adapter factory module.
"""

from src.config import MODEL_REGISTRY
from src.adapters.base import BaseModelAdapter
from src.adapters.jev_adapter import JevAdapter
from src.adapters.laya_adapter import LayaAdapter
from src.adapters.openai_adapter import OpenAIAdapter
from src.adapters.ollama_adapter import OllamaAdapter
from src.adapters.mock_adapter import MockAdapter


def get_adapter(model_name: str) -> BaseModelAdapter:
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model name: {model_name}. Registered models: {list(MODEL_REGISTRY.keys())}")
    
    info = MODEL_REGISTRY[model_name]
    if info.provider == "typesafe":
        return JevAdapter(model_name, info)
    elif info.provider == "laya":
        return LayaAdapter(model_name, info)
    elif info.provider == "openai":
        return OpenAIAdapter(model_name, info)
    elif info.provider == "ollama":
        return OllamaAdapter(model_name, info)
    elif info.provider == "mock":
        return MockAdapter(model_name, info)
    else:
        raise ValueError(f"Unsupported provider {info.provider} for model {model_name}")
