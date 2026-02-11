from secret_key import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
os.environ["OPENAI_API_KEY"] = openai


chat = ChatPromptTemplate.from_messages([
    ("system", "{system}"),
    ("human", "{input}")
])


model = ChatOpenAI()

prompt = chat.format_messages(input="Tell me a joke", system="You are a java developer")
response = model.invoke(prompt)
print(response.content)