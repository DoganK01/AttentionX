from typing import List

from langchain.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.google_scholar import GoogleScholarQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.utilities.google_scholar import GoogleScholarAPIWrapper

from src.settings import CollectionName
from src.prompts import TOOL_DESCRIPTIONS
from src.retrievers import initialize_contextual_compression_retrievers


def initialize_retriever_tools():
    """
    Initialize and return a list of Tool instances for each collection.
    """

    collection_retriever_reranker_map = initialize_contextual_compression_retrievers()

    tools = []
    for collection_name in CollectionName:
        name = collection_name.value
        retriever = collection_retriever_reranker_map.get(collection_name.value)
        description = TOOL_DESCRIPTIONS.get(collection_name)

        tool = create_retriever_tool(retriever=retriever, name=name, description=description)
        tools.append(tool)

    return tools

def initialize_research_search_tools():

    google_scholar = GoogleScholarQueryRun(api_wrapper=GoogleScholarAPIWrapper(top_k_results=10))
    arxiv = ArxivAPIWrapper(top_k_results=10)
    tavily = TavilySearchResults(max_results=10)
    return google_scholar, arxiv, tavily