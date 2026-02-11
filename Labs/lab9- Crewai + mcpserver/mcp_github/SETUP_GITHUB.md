# GitHub MCP Server Setup Guide

## Quick Start

### Step 1: Generate Your GitHub Personal Access Token

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"** button
3. Fill in the form:
   - **Note:** `Lab9 MCP Server` (or any name you prefer)
   - **Expiration:** 90 days (or your preference)
   - **Select scopes:**
     - ✅ `repo` (full control of private repositories)
     - ✅ `user` (read user profile data)
     - ✅ `read:org` (read organization information)

4. Click **"Generate token"**
5. **⚠️ IMPORTANT:** Copy your token immediately (you won't see it again!)

### Step 2: Store Your Token (Choose One Method)

#### Option A: Environment Variable (Recommended)

In PowerShell:
```powershell
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"
```

To persist across sessions (optional):
```powershell
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_xxxxxxxxxxxxxxxxxxxx", "User")
```

#### Option B: Local Configuration File

1. Navigate to `mcp_github` folder
2. Create a `.github_env` file (this is git-ignored):
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
   ```

### Step 3: Verify Your Token

```powershell
# Test the GitHub MCP server
cd "Labs\lab9- Crewai + mcpserver"

# Start the server
uvicorn mcp_github.app:app --port 8003 --reload
```

In another terminal:
```powershell
# Test health endpoint
curl http://localhost:8003/health

# Test user endpoint
curl "http://localhost:8003/user/torvalds"
```

## File Structure

```
mcp_github/
├── app.py                    # FastAPI server with GitHub endpoints
├── config.py                 # Token configuration management
├── __init__.py              # Package initialization
├── README.md                # Detailed documentation
├── .github_env_template     # Template for .github_env file
└── .github_env              # ⚠️ GIT-IGNORED (your actual token goes here)
```

## Security Checklist

- ✅ Token stored in environment variable or `.github_env` (never hardcoded)
- ✅ `.github_env` is in `.gitignore` (never committed)
- ✅ Token is loaded securely in `config.py`
- ✅ No credentials in logs or error messages
- ✅ HTTPS used for all GitHub API calls
- ✅ Type-safe with Pydantic models

## Testing the API

### Get User Information
```bash
curl "http://localhost:8003/user/octocat"
```

### List User Repositories
```bash
curl "http://localhost:8003/user/octocat/repos?limit=5&sort=stars"
```

### Get Repository Issues
```bash
curl "http://localhost:8003/repo/octocat/Hello-World/issues?state=open&limit=10"
```

### Search Repositories
```bash
curl "http://localhost:8003/search/repositories?q=python+language:python&sort=stars&limit=10"
```

## Troubleshooting

### "GITHUB_TOKEN not found" Error

1. Verify you set the environment variable:
   ```powershell
   echo $env:GITHUB_TOKEN
   ```
   Should output your token (usually starts with `ghp_`)

2. If empty, set it again:
   ```powershell
   $env:GITHUB_TOKEN = "ghp_your_token_here"
   ```

3. Or create `.github_env` file in `mcp_github/` directory

### "401 Unauthorized" Error

- Your token may be expired
- Your token may have insufficient permissions
- Generate a new token with required scopes

### "403 Forbidden" Error

- You've hit GitHub's rate limit (5,000 requests/hour for authenticated)
- Wait an hour and try again, or use a token with higher limits

### "502 Bad Gateway" Error

- GitHub API is temporarily unavailable
- Check [GitHub Status](https://www.githubstatus.com/)

## Advanced Usage

### Integrating with CrewAI Agent

See `example_github_agent.py` for how to use the GitHub MCP server with the CrewAI agent.

```python
agent = GitHubAgent()
report = agent.generate_report("username")
```

### Rate Limits

Monitor your rate limit status:
```bash
curl "http://localhost:8003/user/octocat" -i
```

Look for headers:
- `X-RateLimit-Limit: 5000`
- `X-RateLimit-Remaining: 4999`
- `X-RateLimit-Reset: 1234567890`

## Next Steps

1. ✅ Generate your GitHub Personal Access Token
2. ✅ Set `GITHUB_TOKEN` environment variable
3. ✅ Start the MCP server: `uvicorn mcp_github.app:app --port 8003`
4. ✅ Test endpoints with curl or the example agent
5. ✅ Integrate with your CrewAI workflows

## Resources

- [GitHub API Documentation](https://docs.github.com/en/rest?apiVersion=2022-11-28)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Token Scopes](https://docs.github.com/en/developers/apps/scopes-for-oauth-apps)
