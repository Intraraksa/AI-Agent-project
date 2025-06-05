from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
# from utils import nodes
from dotenv import load_dotenv
import os
from typing import Annotated, List, TypedDict
from utils.nodes import content_node, reflection_node, should_continue_node, State
load_dotenv()

workflow = StateGraph(State)
workflow.add_node("content_creator", content_node)
workflow.add_node("reflection", reflection_node)
workflow.add_edge(START, "content_creator"),
workflow.add_conditional_edges("content_creator", 
                            should_continue_node, {
                                "continue": "reflection",
                                "end": END,
                            })
workflow.add_edge("reflection", "content_creator")
graph = workflow.compile()


def main(text_input:str=None):
    result = graph.invoke({"messages": text_input})
    return result



if __name__ == "__main__":
    text_input = input("User : ")
    result = main(text_input)
    print("Agent : ", result["messages"][-1].content)