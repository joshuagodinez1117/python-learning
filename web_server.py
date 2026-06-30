from flask import Flask, jsonify, request
import datetime
import os
import csv
from dotenv import load_dotenv
import requests as http_requests
import sqlite3

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

@app.route("/people/stats")
def people_stats():
    column = request.args.get("column", "age")
    stat = request.args.get("stat", "average")

    people = load_people()
    if not people:
        return jsonify({"error": "No data found"}), 404

    if column not in people[0]:
        return jsonify({"error": f"Column '{column}' not found. Available: {list(people[0].keys())}"}), 400

    try:
        values = [float(row[column]) for row in people]
    except ValueError:
        return jsonify({"error": f"Column '{column}' contains non-numeric data"}), 400

    if stat == "average":
        result = sum(values) / len(values)
    elif stat == "sum":
        result = sum(values)
    elif stat == "min":
        result = min(values)
    elif stat == "max":
        result = max(values)
    elif stat == "count":
        result = len(values)
    else:
        return jsonify({"error": f"Unknown stat '{stat}'. Use: average, sum, min, max, count"}), 400

    return jsonify({
        "column": column,
        "stat": stat,
        "result": result,
        "sample_size": len(values)
    })

@app.route("/query", methods=["POST"])
def query():
    body = request.get_json()
    if not body or "sql" not in body:
        return jsonify({"error": "Request body must include a 'sql' field"}), 400

    sql = body["sql"]

    # Log every query for safety/auditing
    with open("query_log.txt", "a") as log:
        log.write(f"{datetime.datetime.now(datetime.UTC).isoformat()} | {sql}\n")

    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row  # lets us return rows as dicts instead of plain tuples

    try:
        cursor = conn.execute(sql)
        if sql.strip().lower().startswith("select"):
            rows = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return jsonify({"rows": rows, "row_count": len(rows)})
        else:
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return jsonify({"message": "Query executed", "rows_affected": affected})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)