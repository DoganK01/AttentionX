from langchain.agents import AgentExecutor, create_openai_tools_agent
from typing import Any, Dict, TypedDict

from src.tools import initialize_retriever_tools
from src.settings import settings
from src.prompts import Prompts

def get_class():
   return Prompts()

def exe_agent(input):
  tools = initialize_retriever_tools()
  llm = settings.app.LLM_MODEL()
  prompt_class = get_class()
  prompt = prompt_class.make_ready_openai_agent_prompt()

  agent = create_openai_tools_agent(llm, tools, prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
  response=agent_executor.invoke({"input": input})
  return response['intermediate_steps'][0][-1]


def organize_research(findings: Dict[str, Any]) -> str:
    return (
        findings["academic2"] + "\n\n"
        + "\n\n".join([str(result["content"]) for result in findings["tavily"]])
        + findings["academic1"] + "\n\n"
    )