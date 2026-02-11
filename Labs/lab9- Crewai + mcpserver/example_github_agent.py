"""Example: Using GitHub MCP Server with CrewAI Agent.

This example demonstrates how to integrate the GitHub MCP server
with the CrewAI agent for secure GitHub API access.
"""

import httpx
from typing import List


class GitHubAgent:
    """Agent that uses GitHub MCP server for all API calls."""

    def __init__(self, github_mcp_base: str = "http://localhost:8003"):
        self.github_mcp = github_mcp_base.rstrip("/")
        self._client = httpx.Client(timeout=10.0)

    def fetch_user_info(self, username: str) -> dict:
        """Fetch GitHub user information via MCP server."""
        r = self._client.get(f"{self.github_mcp}/user/{username}")
        r.raise_for_status()
        return r.json()

    def fetch_user_repos(self, username: str, limit: int = 5) -> List[dict]:
        """Fetch user repositories via MCP server."""
        r = self._client.get(
            f"{self.github_mcp}/user/{username}/repos",
            params={"limit": limit, "sort": "stars"},
        )
        r.raise_for_status()
        return r.json()

    def fetch_repo_issues(
        self, owner: str, repo: str, state: str = "open", limit: int = 5
    ) -> List[dict]:
        """Fetch repository issues via MCP server."""
        r = self._client.get(
            f"{self.github_mcp}/repo/{owner}/{repo}/issues",
            params={"state": state, "limit": limit},
        )
        r.raise_for_status()
        return r.json()

    def search_repositories(self, query: str, limit: int = 10) -> dict:
        """Search repositories via MCP server."""
        r = self._client.get(
            f"{self.github_mcp}/search/repositories",
            params={"q": query, "limit": limit, "sort": "stars"},
        )
        r.raise_for_status()
        return r.json()

    def generate_report(self, username: str) -> dict:
        """Generate a complete GitHub user report."""
        print(f"\n📊 Generating GitHub report for '{username}'...")

        # Fetch user info
        user = self.fetch_user_info(username)
        print(f"✅ User: {user['login']} ({user['id']})")

        # Fetch repositories
        repos = self.fetch_user_repos(username, limit=5)
        print(f"✅ Top 5 repositories: {len(repos)} found")

        # Fetch issues from top repo (if any public repos)
        issues = []
        if repos:
            top_repo = repos[0]
            owner, repo_name = top_repo["full_name"].split("/")
            try:
                issues = self.fetch_repo_issues(owner, repo_name, limit=5)
                print(f"✅ Open issues in {top_repo['name']}: {len(issues)} found")
            except Exception as e:
                print(f"⚠️  Could not fetch issues: {e}")

        return {
            "user": user,
            "repositories": repos,
            "issues": issues,
        }


def main():
    """Example usage of GitHub MCP Agent."""
    
    # Ensure GitHub MCP server is running on port 8003
    agent = GitHubAgent()
    
    # Example: Get info about Linus Torvalds
    try:
        report = agent.generate_report("torvalds")
        
        print("\n📋 Report Summary:")
        print(f"  User: {report['user']['login']}")
        print(f"  Bio: {report['user']['bio']}")
        print(f"  Repositories: {len(report['repositories'])}")
        for repo in report['repositories']:
            print(f"    - {repo['name']} ⭐ {repo['stars']}")
        
        if report['issues']:
            print(f"  Recent Issues: {len(report['issues'])}")
            for issue in report['issues'][:3]:
                print(f"    - #{issue['number']}: {issue['title']}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️  Make sure GitHub MCP server is running:")
        print("   uvicorn mcp_github.app:app --port 8003 --reload")
        print("\n⚠️  And your GitHub token is set:")
        print("   $env:GITHUB_TOKEN = 'your_token_here'")


if __name__ == "__main__":
    main()
