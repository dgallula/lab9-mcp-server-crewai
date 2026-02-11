# GitHub MCP Server

A single-responsibility MCP (Model Context Protocol) server that provides secure access to the GitHub API.

## Features

- ✅ User information retrieval
- ✅ Repository listing and search
- ✅ Issue tracking
- ✅ Secure API token management (git-ignored)
- ✅ Type-safe responses with Pydantic models
- ✅ FastAPI-based endpoints

## Setup

### 1. Generate GitHub Personal Access Token

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `user` (read user profile)
   - `read:org` (read organization info)
4. Copy your token and save it

### 2. Configure the Token

Choose one of these methods:

#### Method A: Environment Variable (Recommended)
```powershell
$env:GITHUB_TOKEN = "your_token_here"
```

#### Method B: Local Configuration File
Create a `.github_env` file in this directory:
```
GITHUB_TOKEN=your_token_here
```

**⚠️ IMPORTANT:** This file is git-ignored. Never commit your token!

## Running the Server

```powershell
# Install dependencies (if not already installed)
pip install -r ../requirements.txt

# Start the server on port 8003
uvicorn mcp_github.app:app --port 8003 --reload
```

The server will be available at `http://localhost:8003`

## API Endpoints

### Health Check
```
GET /health
```

### User Information
```
GET /user/{username}
Response: GitHubUser (login, id, avatar_url, profile_url, bio)
```

### User Repositories
```
GET /user/{username}/repos?limit=10&sort=stars
Response: List[GitHubRepo] (name, full_name, description, url, stars, language)
```

### Repository Issues
```
GET /repo/{owner}/{repo}/issues?state=open&limit=10
Response: List[GitHubIssue] (number, title, state, created_at, user_login, url)
```

### Search Repositories
```
GET /search/repositories?q=python&sort=stars&limit=10
Response: dict with total_count and items list
```

## Usage Example

```python
import httpx

# Initialize client with GitHub MCP server
github_mcp = "http://localhost:8003"

async def fetch_user_repos():
    async with httpx.AsyncClient() as client:
        # Get user info
        user_resp = await client.get(f"{github_mcp}/user/torvalds")
        user = user_resp.json()
        print(f"User: {user['login']}")
        
        # Get user's repos
        repos_resp = await client.get(f"{github_mcp}/user/torvalds/repos?limit=5")
        repos = repos_resp.json()
        for repo in repos:
            print(f"  - {repo['name']} ({repo['stars']} ⭐)")
```

## Integration with Lab9 Agent

To integrate this server with the CrewAI agent:

1. Update `run_agent.py` to include GitHub MCP server
2. Add GitHub tasks to the agent workflow
3. Agent will call this server for all GitHub API needs

## Security Notes

- ✅ Token is never logged or exposed
- ✅ Token file is git-ignored
- ✅ Environment variable preferred over file storage
- ✅ All API calls use GitHub's secure HTTPS endpoints
- ✅ Proper error handling for rate limiting and auth failures

## Error Handling

- `404`: User or repository not found
- `401`: Invalid or expired token
- `403`: Insufficient permissions or rate limit exceeded
- `502`: GitHub API unavailable

## Rate Limiting

GitHub API free tier:
- Authenticated requests: 5,000/hour
- Unauthenticated: 60/hour

Monitor your usage with:
```
GET /user (includes rate limit headers)
```

## Next Steps

1. ✅ Start the GitHub MCP server on port 8003
2. ✅ Set your GITHUB_TOKEN environment variable
3. ✅ Test endpoints with curl or Postman
4. ✅ Integrate with CrewAI agent
