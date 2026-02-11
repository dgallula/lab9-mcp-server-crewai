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

prompt_template_items = PromptTemplate(
    input_variables=['restaurant_name'],
    template="Suggest some menu items for {restaurant_name}. Return it as a comma seperated list"
)




from langchain_core.output_parsers import StrOutputParser


chain_name = prompt_template_name | model  | StrOutputParser() 
chain_items = prompt_template_items | model | StrOutputParser()

full_chain = chain_name | {
    'name': chain_name,
    'items': chain_items
}

response = full_chain.invoke("Indian")
print(response["name"])
print(response["items"])
