from crewai import Agent, Task, Crew, Process
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from secret_key import OPENAI_API_KEY as api_key
    os.environ["OPENAI_API_KEY"] = api_key
except Exception:
    # rely on externally configured OPENAI_API_KEY
    pass

from tools import repl, file_read_tool




coding_agent = Agent(
	role="Python Developer",
	goal="Craft a well design and thought out code to answer the given problem",
 	backstory=""" 
 				You are a senior Python developer with extensive experience in software and its best practices.
            	You have expertise in writing clean, efficient, and scalable code. 
 			""",
	llm="gpt-4o",
 	tools=[file_read_tool]
)

coding_task = Task(
	description=""" 
 					Write Python code to answer the given problem. 
                	The code should read the CSV file and perform the requested analysis.
                	Make sure to assign the final result to a variable called 'result'.
                    Problem: {problem}
                    Return only the Python code that can be executed directly.
 				""",
     expected_output="Complete python code that solved the problem and assigns output to 'result 'variable ",
	agent=coding_agent,
 	verbose=True
)


#####################################################


executing_agent = Agent(
	role="Python Code Executor",
 goal="Execute python code and return the results",
 backstory="""
				You are a Python developer with extensive experience in software and its best practices.
            	You can execute code, debug, and optimize Python solutions effectively.
	""",
 llm="gpt-4o",
 tools=[repl],
 verbose=True
)

executing_task = Task(
	description=""" Execute the python code provided by the coding agent to solve the given problem""",
	expected_output="The actual execution results",
	agent=executing_agent, 
	context=[coding_task] # This ensures the exeucting task gets the output from the coding task.
)

inputs = {'problem': "Read the people.csv (C:\\Users\\דוד גלולה\\Desktop\\KIVUN - AI\\Labs\\Lab8 - CrewAI\\Lab\\people.csv) file and create a code that returns the column names and find the mean age." }

crew = Crew(
	agents=[coding_agent, executing_agent],
	tasks=[coding_task, executing_task],
	verbose=True,
	process=Process.sequential
)

result = crew.kickoff(inputs=inputs)
print(result.raw)

