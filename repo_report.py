import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("GITHUB_TOKEN")
repo = "joshuagodinez1117/python-learning"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

def get_commits(repo, limit=10):
    url = f"https://api.github.com/repos/{repo}/commits"
    response = requests.get(url, headers=headers, params={"per_page": limit})
    if response.status_code != 200:
        print(f"Failed to get commits: {response.status_code}")
        return []
    return response.json()

def get_pull_requests(repo, state="all"):
    url = f"https://api.github.com/repos/{repo}/pulls"
    response = requests.get(url, headers=headers, params={"state": state})
    if response.status_code != 200:
        print(f"Failed to get PRs: {response.status_code}")
        return []
    return response.json()

def get_repo_summary(repo):
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get repo info: {response.status_code}")
        return {}
    return response.json()

# --- Run the report ---
print("=" * 50)
print(f"REPOSITORY REPORT: {repo}")
print("=" * 50)

# Summary
summary = get_repo_summary(repo)
if summary:
    print(f"\nDescription: {summary['description']}")
    print(f"Default branch: {summary['default_branch']}")
    print(f"Open issues: {summary['open_issues_count']}")
    print(f"Last updated: {summary['updated_at']}")

# Recent commits
print(f"\n--- LAST 10 COMMITS ---")
commits = get_commits(repo, limit=10)
for commit in commits:
    sha = commit['sha'][:7]
    message = commit['commit']['message'].split('\n')[0]
    author = commit['commit']['author']['name']
    date = commit['commit']['author']['date']
    print(f"{sha} | {date} | {author} | {message}")

# Pull requests
print(f"\n--- PULL REQUESTS ---")
prs = get_pull_requests(repo, state="all")
if not prs:
    print("No pull requests found.")
else:
    for pr in prs:
        number = pr['number']
        title = pr['title']
        state = pr['state']
        created = pr['created_at']
        merged = pr.get('merged_at', None)
        print(f"#{number} [{state.upper()}] {title}")
        print(f"       Created: {created}")
        if merged:
            print(f"       Merged:  {merged}")

print("\n" + "=" * 50)