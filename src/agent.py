import os
import inspect

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import AIMessage, HumanMessage
from langchain_core.tools import BaseTool

from tools import Tools

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
tools = []
methods = inspect.getmembers(Tools, predicate=lambda m: isinstance(m, BaseTool))
for method_name, method in methods:
    tools.append(method)

# print(tools[1].invoke({'paper_id': "arXiv:2603.21852", "output_options": None}))

model = ChatOpenAI(model="deepseek/deepseek-v4-flash",
                     base_url="https://openrouter.ai/api/v1", api_key=API_KEY)
        
agent = create_agent(model, tools=tools)

for chunk in agent.stream({
    "messages": [
        HumanMessage(content="Test123"),
    ]
}, stream_mode="updates", version="v2"):
    # print(chunk)
        if chunk["type"] == "updates":
            for step, data in chunk["data"].items():
                print(f"step: {step}")
                print(f"content: {data['messages'][-1].content_blocks}")