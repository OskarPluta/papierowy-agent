import inspect

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import AIMessage, HumanMessage
from langchain_core.tools import BaseTool

from tools import Tools

load_dotenv()
tools = []
methods = inspect.getmembers(Tools, predicate=lambda m: isinstance(m, BaseTool))
for method_name, method in methods:
    tools.append(method)


model = ChatOpenAI(model="deepseek/deepseek-v4-flash:free",
                     base_url="https://openrouter.ai/api/v1",)
        
agent = create_agent(model, tools=tools)

for chunk in agent.stream({
    "messages": [
        HumanMessage(content="Try to find a connections with this paper to a different one: arXiv:2603.21852v2. Use available tools"),
    ]
}, stream_mode="values"):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"Human: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"AI: {latest_message.content}")
    elif latest_message.tool_calls:
        for tool_call in latest_message.tool_calls:
            print(f"Tool call: {tool_call['name']} with arguments {tool_call['args']}")
