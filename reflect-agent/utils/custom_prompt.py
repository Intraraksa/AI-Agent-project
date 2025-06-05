from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState

from dotenv import load_dotenv
import os
load_dotenv()
# Load environment variables

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """ You are content creator agent. you are expert in creating content for 
                       LinkedIn posts, You content must be useful for the users and should be engaging.
                       Recruiters and hiring managers are your target audience.
                       Your task is to create a LinkedIn post based on the provided messages."""),
        ("human", " please create content about {messages}"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """ You are senior content creator agent. you have to critically analyze the content created by the content creator agent.
                       You must provide feedback on the content, suggest improvements, and ensure that it is engaging and useful for the target audience.
                       Recruiters and hiring managers are your target audience."""),
         
        ("human", "{messages}"),
    ]
)

class AgentPrompt:
    def __init__(self):
        self.generation_prompt = generation_prompt
        self.reflection_prompt = reflection_prompt

    def content_generation(self, input_text: str=None) -> ChatPromptTemplate:

        if input_text is None:
            return self.generation_prompt
        else:
            self.generation_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", input_text),
                    ("human", "{messages}"),
                ]
            )
            return self.generation_prompt
        
    def content_reflection(self, input_text: str=None) -> ChatPromptTemplate:
        if input_text is None:
            return self.reflection_prompt
        else:
            self.reflection_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", input_text),
                    ("human", "{messages}"),
                ]
            )
            return self.reflection_prompt