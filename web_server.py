from flask import Flask, jsonify
import datetime
import os
import csv
from dotenv import load_dotenv
import requests as http_requests

load_dotenv()

app = Flask(__name__)

def load_people():
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
        pass
    return people

def get_github_summary():
    token = os.environ.get("GITHUB_TOKEN")
    repo = "joshuagodinez1117/python-learning"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    response = http_requests.get(
        f"https://api.github.com/repos/{repo}",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return {
            "repo": data["full_name"],
            "description": data["description"],
            "default_branch": data["default_branch"],
            "open_issues": data["open_issues_count"],
            "last_updated": data["updated_at"]
        }
    return {"error": f"GitHub API returned {response.status_code}"}

@app.route("/")
def home():
    return "Hello from your Python web server!"

@app.route("/status")
def status():
    return jsonify({
        "status": "running",
        "message": "Server is operational",
        "time": datetime.datetime.now(datetime.UTC).isoformat()
    })

@app.route("/people")
def people():
    return jsonify(load_people())

@app.route("/github")
def github():
    return jsonify(get_github_summary())

@app.route("/report")
def report():
    return jsonify({
        "people": load_people(),
        "github": get_github_summary(),
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)