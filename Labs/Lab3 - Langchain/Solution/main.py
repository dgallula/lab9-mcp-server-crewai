

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = ""  # Set your OpenAI API key

model = ChatOpenAI()

prompt_template_code = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a very experienced python developer that keen of writing a very short and efficient code"),
        
        ("human", "Write code for {app_goal}, return only the code withoout extra explanation or text")
    ]
)

prompt_template_unit_test = PromptTemplate(
    input_variables=["code"],
    template="Write proper unit test for the following code: {code}, return only the tests code without any extra text "
)


chain_code = prompt_template_code | model | StrOutputParser()
chain_tests = prompt_template_unit_test | model | StrOutputParser()

full_chain = chain_code |  {
    "code": chain_code,
    "tests": chain_tests
}

result = full_chain.invoke({"app_goal": "Sorting an array of numbers"})
print("######### CODE ########")
print(result["code"])

print("######### TESTS ########")
print(result["tests"])
