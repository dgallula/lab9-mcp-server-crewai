from crewai import Agent, Task, Crew
import os
os.environ["OPENAI_API_KEY"] = "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"


info_agent = Agent(
    role="You are an infromation Agent",
    goal="Give compelling information about a certain topic",
    backstory="You know to love information, People love and hate you for that, you win most of the quizzes at your local pub",
    verbose=True
)

task1 = Task(
    description="Tell me all about the great white shark",
    expected_output="Give me a quick summary with at least 7 bullet points",
    agent=info_agent
)

crew = Crew(
    agents=[info_agent],
    tasks=[task1],
    verbose=True
)

result = crew.kickoff()
print("###################")
print(result)