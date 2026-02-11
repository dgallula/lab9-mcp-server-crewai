from typing import List

from fastapi import FastAPI, HTTPException, Query
import httpx

app = FastAPI(title="MCP External Proxy")


@app.get("/fetch/jsonplaceholder/posts")
async def fetch_jsonplaceholder_posts(limit: int = Query(10, ge=1, le=100)) -> List[dict]:
    """Fetch posts from JSONPlaceholder and return a list of items.

    This MCP server is the only component that calls the external JSONPlaceholder API.
    The agent must call this MCP tool rather than calling JSONPlaceholder directly.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream JSONPlaceholder failed")
    data = r.json()[:limit]
    # normalize lightly for the agent; agent will perform final normalization
    return [{"source": "jsonplaceholder", "raw": item} for item in data]


@app.get("/fetch/dummyjson/products")
async def fetch_dummyjson_products(limit: int = Query(10, ge=1, le=100)) -> List[dict]:
    """Fetch products from DummyJSON.

    Returns: list of {source, raw}
    """
    url = "https://dummyjson.com/products"
    params = {"limit": limit}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream DummyJSON failed")
    body = r.json()
    items = body.get("products", [])
    return [{"source": "dummyjson", "raw": item} for item in items]


@app.get("/fetch/tvmaze/shows")
async def fetch_tvmaze_shows(q: str = Query("girls"), limit: int = Query(10, ge=1, le=100)) -> List[dict]:
    """Search TVMaze shows (default query 'girls' to keep deterministic results).

    Returns list of {source, raw}
    """
    url = "https://api.tvmaze.com/search/shows"
    params = {"q": q}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream TVMaze failed")
    data = r.json()[:limit]
    # TVMaze search returns [{"score":..., "show": {...}}]
    items = [entry.get("show") for entry in data if isinstance(entry, dict) and "show" in entry]
    return [{"source": "tvmaze", "raw": item} for item in items]
