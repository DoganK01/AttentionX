from enum import Enum
from typing import List

from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic_settings import BaseSettings

from src.cohere_rerank import CohereRerank


class CollectionName(Enum):
    QDRANT_RAG = "QDRANT_RAG"



class EnvironmentSettings(BaseSettings):
    LANGCHAIN_TRACING_V2: str
    LANGCHAIN_PROJECT: str
    LANGCHAIN_API_KEY: str
    BROWSERLESS_API_KEY: str
    QDRANT__URL: str
    QDRANT__API_KEY: str
    OPENAI_API_KEY: str
    COHERE_API_KEY: str
    TAVILY_API_KEY: str
    LLAMA_PARSE_API_KEY: str
    GOOGLE_API_KEY: str
    ARXIV_API_KEY: str

    class Config:
        env_file = ".env"


class AppSettings(BaseSettings):
    COLLECTION_NAMES: List[CollectionName] = list(CollectionName)

    @property
    def LLM_MODEL(self) -> ChatOpenAI:
        return ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

    @property
    def EMBEDDING_MODEL(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(model="text-embedding-3-large")

    @property
    def RERANKER_MODEL(self) -> CohereRerank:
        return CohereRerank(top_n=5)


class Settings(BaseSettings):
    env: EnvironmentSettings = EnvironmentSettings()
    app: AppSettings = AppSettings()

    @property
    def qdrant_args(self):
        return {
            "url": self.env.QDRANT__URL,
            "api_key": self.env.QDRANT__API_KEY,
            "prefer_grpc": True,
        }


settings = Settings()