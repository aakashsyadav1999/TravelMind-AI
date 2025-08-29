from langchain_openai import ChatOpenAI
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    model_name: str
    temperature: float
    max_tokens: int
    request_timeout: Optional[int] = None
    streaming: bool = True

    @classmethod
    def create_balanced_config(cls) -> 'LLMConfig':
        return cls(
            model_name="gpt-4o-mini",
            temperature=0.7,
            max_tokens=200,
            request_timeout=15
        )

    @classmethod
    def create_fast_config(cls) -> 'LLMConfig':
        return cls(
            model_name="gpt-4o-mini",
            temperature=0.5,
            max_tokens=200,
            request_timeout=15
        )

    def create_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            request_timeout=self.request_timeout
        )
