from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import add_messages
from .custom_prompt import AgentPrompt

from dotenv import load_dotenv
import os
from typing import Annotated, List, TypedDict
# Load environment variables
load_dotenv()

agent_prompt = AgentPrompt()
generation_prompt = agent_prompt.content_generation(input_text=None)
reflection_prompt = agent_prompt.content_reflection(input_text=None)

# Define the state for the graph
class State(TypedDict):
    messages: Annotated[List, add_messages]

# Define the content_node for the graph
def content_node(state: State):

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.3)
    # llm = ChatOpenAI(model="o4-mini-2025-04-16")

    chain = generation_prompt | llm

    result = chain.invoke([state["messages"]])

    return {"messages": result}

# Define the reflection node for the graph
def reflection_node(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.1)
    # llm = ChatOpenAI(model="o4-mini-2025-04-16")

    chain = reflection_prompt | llm

    result = chain.invoke([state["messages"]])

    return {"messages": result}

def should_continue_node(state: State):
    # This node can be used to determine if the process should continue
    # For now, we will just return True to indicate continuation
    if len(state["messages"]) > 7:
        return "end"
    return "continue"


