import argparse
import asyncio
import glob
import json
import os
import re
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient, AsyncQdrantClient, models
from langchain_experimental.text_splitter import SemanticChunker
from llama_parse import LlamaParse
from src.settings import CollectionName, settings

load_dotenv()

# Define model dimensions for easy reference and validation
MODEL_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
}


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Upload chunks of text data to Qdrant.")
    parser.add_argument("--folder", type=str, required=True, help="The folder containing the text data.")
    parser.add_argument(
        "--collection_name", type=str, required=True, help="The name of the collection to create in Qdrant."
    )
    parser.add_argument(
        "--embedding_model",
        type=str,
        required=True,
        choices=list(MODEL_DIMENSIONS.keys()),
        help="The name of the embedding model to use.",
    )
    return parser.parse_args()


async def load_documents(folder: str) -> List[Document]:
    """
    Prepare documents from text files and metadata.

    Args:
        folder (str): Folder containing text files and metadata.
        

    Returns:
        List[Document]: List of Document objects ready for chunking.
    """
    # Parse documents using LlamaParse
    parser = LlamaParse(
        api_key=settings.env.LLAMA_PARSE_API_KEY,
        result_type="markdown",
        verbose=True,
        language="en"
    )
    docs = await parser.aload_data(file_path=str(folder / f"Virus.pdf"))
    return docs


async def prepare_documents(documents: List[Document], model_name: str) -> List[Document]:
    """
    Split documents into chunks.
    Args:
        documents (List[Document]): List of Document objects.
    """
    text_splitter = SemanticChunker(embeddings=OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.env.OPENAI_API_KEY))
    splitted_documents = await text_splitter.atransform_documents(documents=[Document(page_content=doc.text) for doc in documents])
    
    #splitted_docs = text_splitter.create_documents([Document(page_content=doc.text) for doc in documents])
    return splitted_documents


async def main(folder, collection_name: str, embedding_model: str) -> None:
    """
    Main function to process documents and upload them to Qdrant.

    Args:
        collection_name (str): Name of the collection in Qdrant.
        embedding_model (str): Embedding model to use for document vectors.
    """
    client = AsyncQdrantClient(settings.env.OPENAI_API_KEY)


    await client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=MODEL_DIMENSIONS[embedding_model], distance=models.Distance.COSINE),
    )

    documents = load_documents(folder)
    documents = await prepare_documents(documents)
    embeddings = OpenAIEmbeddings(model=embedding_model, openai_api_key=settings.env.OPENAI_API_KEY)

    vector_store = Qdrant(
        client=QdrantClient(settings.env.OPENAI_API_KEY),
        async_client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    await vector_store.aadd_documents(documents=documents)



if __name__ == "__main__":
    args = parse_arguments()
    asyncio.run(
        main(
            folder=args.folder,
            collection_name=args.collection_name,
            embedding_model=args.embedding_model
        )
    )