import csv
import os
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests

load_dotenv()

mcp = FastMCP("python-learning-tools")

@mcp.tool()
def get_people() -> str:
    """Load and return all people from people.csv as a JSON string."""
    people = []
    try:
        with open("people.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["age"] = int(row["age"])
                    people.append(row)
                except ValueError:
                    pass
    except FileNotFoundError:
        return "Error: people.csv not found"
    return json.dumps(people)

@mcp.tool()
def get_github_summary() -> str:
    """Get a summary of the python-learning GitHub repository."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = "joshuagodinez1117/python-learning"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(
        f"https://api.github.com/repos/{repo}",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        summary = {
            "repo": data["full_name"],
            "description": data["description"],
            "default_branch": data["default_branch"],
            "open_issues": data["open_issues_count"],
            "last_updated": data["updated_at"]
        }
        return json.dumps(summary)
    return f"Error: GitHub API returned {response.status_code}"

if __name__ == "__main__":
    mcp.run()