from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="nvidia/nemotron-3-nano-30b-a3b:free",
                     base_url="https://openrouter.ai/api/v1",)


