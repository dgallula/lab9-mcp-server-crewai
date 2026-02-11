"""GitHub API configuration.

Store your GitHub API token here.
This file is git-ignored for security reasons.
"""

import os

# Get GitHub token from environment variable or .env file
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Optional: Load from a local .env-like file (git-ignored)
if not GITHUB_TOKEN:
    try:
        with open(".github_env", "r") as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    GITHUB_TOKEN = line.split("=")[1].strip()
                    break
    except FileNotFoundError:
        pass

if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN not found. Please set it in:\n"
        "1. Environment variable: GITHUB_TOKEN\n"
        "2. Or create a .github_env file with: GITHUB_TOKEN=your_token_here"
    )
