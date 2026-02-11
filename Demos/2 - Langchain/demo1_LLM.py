from secret_key import openai
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = openai

llm = ChatOpenAI(temperature=1)
response = llm.invoke("I want to open a fancy restaurant for Italian food. Suggest a fancy name for it.")
print(response.content)