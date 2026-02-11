from secret_key import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
os.environ["OPENAI_API_KEY"] = openai


model = ChatOpenAI(temperature=1.0)

prompt_template_name = PromptTemplate(
    input_variables=['cuisine'],
    template="I want to open a fancy restaurant for {cuisine} food. Suggest a fancy name for it."
)

user_cuisine = input("Cuisine avocado!!!: ")
prompt = prompt_template_name.format(cuisine=user_cuisine)

response = model.invoke(prompt)
print(response.content)