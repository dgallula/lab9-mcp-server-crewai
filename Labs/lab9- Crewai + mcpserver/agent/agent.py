"""CrewAI-style agent that only talks to MCP tools.

The agent is deterministic and performs these steps in order:
1. Fetch posts from JSONPlaceholder via MCP external server
2. Fetch products from DummyJSON via MCP external server
3. Fetch shows from TVMaze via MCP external server (fixed query 'girls')
4. Normalize all records into a common schema
5. Insert normalized records into the DB via MCP DB server

The agent never calls external APIs or the DB directly.
"""
from typing import List
import httpx
from pydantic import BaseModel


class NormalizedItem(BaseModel):
    external_id: str
    source: str
    title: str
    body: str = ""
    extra: dict = {}


class Agent:
    """Simple deterministic agent.

    Parameters:
    - external_base: base URL for MCP external server (e.g. http://localhost:8001)
    - db_base: base URL for MCP DB server (e.g. http://localhost:8002)
    """

    def __init__(self, external_base: str, db_base: str, http_timeout: float = 10.0):
        self.external_base = external_base.rstrip("/")
        self.db_base = db_base.rstrip("/")
        self._client = httpx.Client(timeout=http_timeout)

    def fetch_all(self) -> List[dict]:
        """Fetches data from all external API MCP endpoints in a deterministic order."""
        results = []
        # 1. JSONPlaceholder posts
        r1 = self._client.get(f"{self.external_base}/fetch/jsonplaceholder/posts", params={"limit": 5})
        r1.raise_for_status()
        results.extend(r1.json())

        # 2. DummyJSON products
        r2 = self._client.get(f"{self.external_base}/fetch/dummyjson/products", params={"limit": 5})
        r2.raise_for_status()
        results.extend(r2.json())

        # 3. TVMaze shows (fixed query 'girls')
        r3 = self._client.get(f"{self.external_base}/fetch/tvmaze/shows", params={"q": "girls", "limit": 5})
        r3.raise_for_status()
        results.extend(r3.json())

        return results

    @staticmethod
    def normalize_record(record: dict) -> NormalizedItem:
        """Normalize a single {source, raw} entry into `NormalizedItem`."""
        source = record.get("source")
        raw = record.get("raw", {}) or {}
        # Branch with clear mappings per source
        if source == "jsonplaceholder":
            external_id = str(raw.get("id", ""))
            title = raw.get("title", "").strip()
            body = raw.get("body", "").strip()
            extra = {"userId": raw.get("userId")}
        elif source == "dummyjson":
            external_id = str(raw.get("id", ""))
            title = raw.get("title") or raw.get("brand") or ""
            body = raw.get("description", "")
            extra = {"price": raw.get("price")}
        elif source == "tvmaze":
            external_id = str(raw.get("id", ""))
            title = raw.get("name", "")
            summary = raw.get("summary") or ""
            # remove HTML tags crudely (tvmaze sometimes returns HTML in summary)
            body = summary.replace("<p>", "").replace("</p>", "").strip()
            extra = {"type": raw.get("type")}
        else:
            external_id = str(raw.get("id", ""))
            title = str(raw.get("title", "") or raw.get("name", ""))
            body = str(raw.get("body", "") or raw.get("description", ""))
            extra = {}
        return NormalizedItem(external_id=external_id, source=source, title=title, body=body, extra=extra)

    def run(self) -> dict:
        """Main run method: fetch, normalize, insert.

        Returns a summary dict with counts.
        """
        raw_items = self.fetch_all()
        normalized = []
        for r in raw_items:
            item = self.normalize_record(r)
            # simple deterministic filter: skip items without a title
            if item.title:
                normalized.append(item.dict())
        # Insert into DB MCP
        r = self._client.post(f"{self.db_base}/insert/items", json=normalized)
        r.raise_for_status()
        res = r.json()
        return {"fetched": len(raw_items), "to_insert": len(normalized), "db_response": res}
