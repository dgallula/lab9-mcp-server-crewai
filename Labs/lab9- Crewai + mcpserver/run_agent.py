"""Entry point to run the agent against local MCP servers.

Usage (from project root):

# Start external MCP in one terminal
uvicorn mcp_external.app:app --port 8001 --reload

# Start DB MCP in another terminal
uvicorn mcp_db.app:app --port 8002 --reload

# Then run the agent
python run_agent.py

The script will call the MCP servers and print a concise summary.
"""
from crew.crew import Crew
from agent.agent import Agent


def main():
    external = "http://localhost:8001"
    db = "http://localhost:8002"
    agent = Agent(external_base=external, db_base=db)
    crew = Crew()
    crew.add(agent)
    results = crew.run()
    print("Agent run summary:")
    for k, v in results.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
