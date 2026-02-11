"""GitHub MCP Server - Single responsibility: GitHub API access.

This MCP server is the only component that calls the GitHub API.
The agent must call this MCP tool rather than calling GitHub directly.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
import httpx
from pydantic import BaseModel

# Import GitHub token from config (git-ignored)
try:
    from .config import GITHUB_TOKEN
except ImportError:
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    if not GITHUB_TOKEN:
        raise ValueError(
            "GITHUB_TOKEN not configured. Please set GITHUB_TOKEN environment variable."
        )

app = FastAPI(title="MCP GitHub Proxy")

GITHUB_API_BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


class GitHubUser(BaseModel):
    login: str
    id: int
    avatar_url: str
    profile_url: str
    bio: Optional[str] = None


class GitHubRepo(BaseModel):
    name: str
    full_name: str
    description: Optional[str] = None
    url: str
    stars: int
    language: Optional[str] = None


class GitHubIssue(BaseModel):
    number: int
    title: str
    state: str
    created_at: str
    updated_at: str
    user_login: str
    url: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "GitHub MCP server is running"}


@app.get("/user/{username}", response_model=GitHubUser)
async def get_user(username: str):
    """Fetch GitHub user information.
    
    This MCP server is the only component that calls the GitHub API.
    The agent must call this MCP tool rather than calling GitHub directly.
    """
    url = f"{GITHUB_API_BASE}/users/{username}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, headers=HEADERS)
    
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="GitHub API request failed")
    
    data = r.json()
    return GitHubUser(
        login=data["login"],
        id=data["id"],
        avatar_url=data["avatar_url"],
        profile_url=data["html_url"],
        bio=data.get("bio"),
    )


@app.get("/user/{username}/repos", response_model=List[GitHubRepo])
async def get_user_repos(
    username: str,
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("stars", regex="^(stars|updated|created)$"),
):
    """Fetch user's repositories.
    
    Returns: list of repositories sorted by specified criteria
    """
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    params = {
        "sort": sort,
        "direction": "desc",
        "per_page": limit,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, headers=HEADERS, params=params)
    
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="GitHub API request failed")
    
    repos = r.json()
    return [
        GitHubRepo(
            name=repo["name"],
            full_name=repo["full_name"],
            description=repo.get("description"),
            url=repo["html_url"],
            stars=repo["stargazers_count"],
            language=repo.get("language"),
        )
        for repo in repos
    ]


@app.get("/repo/{owner}/{repo}/issues", response_model=List[GitHubIssue])
async def get_repo_issues(
    owner: str,
    repo: str,
    state: str = Query("open", regex="^(open|closed|all)$"),
    limit: int = Query(10, ge=1, le=100),
):
    """Fetch repository issues.
    
    Returns: list of issues with metadata
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": limit,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, headers=HEADERS, params=params)
    
    if r.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"Repository '{owner}/{repo}' not found"
        )
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="GitHub API request failed")
    
    issues = r.json()
    return [
        GitHubIssue(
            number=issue["number"],
            title=issue["title"],
            state=issue["state"],
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
            user_login=issue["user"]["login"],
            url=issue["html_url"],
        )
        for issue in issues
    ]


@app.get("/search/repositories", response_model=dict)
async def search_repositories(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("stars", regex="^(stars|forks|updated)$"),
):
    """Search GitHub repositories.
    
    Returns: search results with repository metadata
    """
    url = f"{GITHUB_API_BASE}/search/repositories"
    params = {
        "q": q,
        "sort": sort,
        "order": "desc",
        "per_page": limit,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, headers=HEADERS, params=params)
    
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="GitHub API search failed")
    
    data = r.json()
    return {
        "total_count": data["total_count"],
        "items": [
            {
                "name": item["name"],
                "full_name": item["full_name"],
                "url": item["html_url"],
                "description": item.get("description"),
                "stars": item["stargazers_count"],
                "language": item.get("language"),
            }
            for item in data["items"]
        ],
    }
