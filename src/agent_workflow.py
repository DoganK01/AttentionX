
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langgraph.graph import END, StateGraph
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from typing_extensions import Annotated

from src.agent_state import ReflectionState, Feedback
from src.settings import settings
from src.tools import initialize_research_search_tools
from src.utils import exe_agent, organize_research
from src.prompts import Prompts

class AgentWorkflow(BaseModel):
    
    llm: Annotated[object, Field(default=settings.app.LLM_MODEL())]
    google_scholar, arxiv, tavily = initialize_research_search_tools()
    prompts_object: Annotated[object, Field(default=Prompts())]
    prompt_general = ChatPromptTemplate.from_messages(messages=[("system", "You are a helpfull assistant"), ("user", prompts_object.USER_PROMPT)])


    def graph_agent(self):
        """
        This function creates a state graph for the agent workflow.
        """
        workfloww = StateGraph(ReflectionState)

        workfloww.add_node("prompt_generator", self.get_relevant_informations)
        workfloww.add_node("response_generator", self.generate_response)
        workfloww.add_node("response_reviewer", self.review_response)
        workfloww.add_node("response_fixer", self.fix_response)

        workfloww.add_edge(start_key="prompt_generator", end_key="response_generator")
        workfloww.add_edge(start_key="response_generator", end_key="response_reviewer")
        workfloww.add_edge(start_key="response_fixer", end_key="response_reviewer")

        workfloww.add_conditional_edges(
            "response_reviewer",
            self.should_fix_response,
            {
                "improve": "response_fixer",
                "end": END
            }
        )

        workfloww.set_entry_point("prompt_generator")
        app = workfloww.compile(debug=True)

        out = RunnableLambda(name="Answer Extraction", func=lambda state: state["keys"]["response"])
        return (app | out)
    
    async def get_relevant_informations(self, state):
        rag_chain = (
            RunnableParallel(academic1=self.google_scholar, academic2=RunnableLambda(func=lambda x: self.arxiv.run(x), name="Arxiv"), tavily=self.tavily, documents=RunnableLambda(func=exe_agent, name="get_docs"), question=RunnablePassthrough())
            | {"research": RunnableLambda(func=organize_research, name="organize_research"), "question": itemgetter("question"), "documents": itemgetter("documents")}
            | self.prompt_general
        )
        actual_prompt = await rag_chain.ainvoke(input=state["keys"]["question"])
        return {"keys": {"question": state["keys"]["question"], "actual_prompt": actual_prompt.messages[1].content}}
        

    async def generate_response(self, state):
        prompt_generate = ChatPromptTemplate.from_messages(
            messages=[
                ("system", self.prompts_object.GENERATOR_SYSTEM_PROMPT),
                ("user", "<topic> {topic} </topic>"+ "\n\n" + state["keys"]["actual_prompt"])
            ]
        )
        runnable = prompt_generate | self.llm | StrOutputParser()
        print(type(state["keys"]["actual_prompt"]))
        #response = await runnable.ainvoke(input={"question": state["keys"]["question"]})
        response = await runnable.ainvoke({"topic": "Healthcare"})
        return {"keys": {"question": state["keys"]["question"], "actual_prompt": state["keys"]["actual_prompt"], "response": response}, "iteration": 0}


    async def review_response(self, state):
        prompt_review = ChatPromptTemplate.from_messages(
            messages=[
                ("system", self.prompts_object.REVIEWER_SYSTEM_PROMPT),
                ("user", state["keys"]["actual_prompt"] + "\n\n" + "<response> {response} </response>")
            ]
        )
        runnable = prompt_review | self.llm.with_structured_output(Feedback)
        feedback = await runnable.ainvoke(input={"response": state["keys"]["response"]})

        return {"keys": {**state["keys"], "feedback": feedback}, "iteration": state["iteration"]}
    
    async def fix_response(self, state):
        prompt_fix = ChatPromptTemplate.from_messages(
            messages=[
                ("system", self.prompts_object.FIXER_SYSTEM_PROMPT),
                ("user", state["keys"]["actual_prompt"] + "\n\n <response> {response} </response>\n\n <feedback> {feedback} </feedback>")
            ]
        )
        runnable = prompt_fix | self.llm | StrOutputParser()
        improved_response = await runnable.ainvoke(input={
            "response": state["keys"]["response"],
            "feedback": state["keys"]["feedback"].suggestions
        })
        return {"keys": {"question": state["keys"]["question"], "actual_prompt": state["keys"]["actual_prompt"], "response": improved_response}, "iteration": state["iteration"] + 1}
    
    def should_fix_response(self, state):
        if any([state["iteration"] >= 5, not state["keys"]["feedback"].has_suggestions]):
            return "end"
        return "improve"
        
