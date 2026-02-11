CrewAI MCP exercise
====================

Overview
--------
This small exercise demonstrates a clean separation between a CrewAI-like agent and two MCP servers:

- `mcp_external`: single-responsibility MCP server that proxies selected public APIs (JSONPlaceholder, DummyJSON, TVMaze).
- `mcp_db`: single-responsibility MCP server that performs all database operations against a local SQLite DB.
- `agent`: deterministic agent that fetches from `mcp_external`, normalizes data, and inserts via `mcp_db`.
- `crew`: minimal orchestrator that runs the agent deterministically.

Design constraints followed:
- The agent never calls external APIs or the DB directly — all calls go through MCP servers.
- Each MCP server has a single responsibility.
- Simple, readable, deterministic code.

Files
-----
- `mcp_external/app.py` — FastAPI MCP server that proxies external APIs.
- `mcp_db/app.py` — FastAPI MCP server that inserts/reads from SQLite.
- `agent/agent.py` — Deterministic agent implementation.
- `crew/crew.py` — Tiny orchestrator.
- `run_agent.py` — Entry point for running the agent after starting MCP servers.
- `requirements.txt` — Python dependencies.

Quickstart
----------
1. Create and activate a virtualenv (recommended).

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the MCP servers in two separate terminals.

Terminal 1 (External MCP):

```powershell
uvicorn mcp_external.app:app --port 8001 --reload
```

Terminal 2 (DB MCP):

```powershell
uvicorn mcp_db.app:app --port 8002 --reload
```

3. Run the agent (after both servers are up):

```powershell
python run_agent.py
```

4. Inspect inserted rows

Open: `http://localhost:8002/items`

Notes
-----
- The project is intentionally minimal for educational use. The `crew` module mimics a CrewAI orchestrator for clarity and does not depend on external CrewAI packages.
- All HTTP tool calls are synchronous/deterministic; no randomness is introduced.
- Inline comments highlight design choices.

Next ideas
----------
- Add unit tests for normalization functions.
- Replace SQLite with PostgreSQL via a dedicated MCP server when expanding the exercise.
