from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

from mcp import StdioServerParameters
import os
os.environ["OPENAI_API_KEY"] = "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"


servers_params = [
    StdioServerParameters(
    command="python",
    args=["C:\\Users\\דוד גלולה\\Desktop\\AI KIVUN\\5 - Agents\\CrewAI\\Demo3_MCP_CrewAI\\mcp_server\\math_mcp_server.py"]),
    
    StdioServerParameters(
        command="python",
        args=["C:\\Users\\דוד גלולה\\Desktop\\AI5 -PUBLIC\\Demos\\MCP\\Demo2_NameOriginMCP\\main.py"]
    )
]


def run_demo(tools):
    agent = Agent(
        role="Mathematician",
        goal="Perform mathemtical operations",
        backstory="An expert in mathematics, capable of performing complex calculations quickly and accurately.",
        tools=tools,
        verbose=True
    )

    task = Task(
        description="Solve the math problem given to you: {problem}",
        expected_output="The correct answer to the math problem using your available tools.",
        agent=agent
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    result = crew.kickoff(inputs={"problem": "What is 4 multiplied by 2?, then tell me what is the origin of the name 'Avi'? in a list."})
    try:
        print("Final Result:", result.raw)
    except Exception:
        print("Final Result:", result)


try:
    with MCPServerAdapter(servers_params) as tools:
        run_demo(tools)
except Exception as e:
    print("MCP servers unavailable or failed to start:", e)
    print("Falling back to running the demo without external MCP tools (no external tool calls).")
    run_demo(None)
        