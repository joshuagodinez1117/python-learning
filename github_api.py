import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("GITHUB_TOKEN")

if not token:
    print("Error: GITHUB_TOKEN environment variable not set.")
    exit(1)

repo = "joshuagodinez1117/python-learning"
url = f"https://api.github.com/repos/{repo}"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Repository: {data['full_name']}")
    print(f"Description: {data['description']}")
    print(f"Default branch: {data['default_branch']}")
    print(f"Stars: {data['stargazers_count']}")
    print(f"Open issues: {data['open_issues_count']}")
    print(f"Created: {data['created_at']}")
    print(f"Last updated: {data['updated_at']}")
    print(f"Rate limit remaining: {response.headers['X-RateLimit-Remaining']}")
else:
    print(f"Request failed: {response.status_code}")
    print(response.json().get("message", "No message returned"))