import sqlite3
import csv

def create_people_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

def load_people_csv(conn, csv_path):
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        rows = [(row["name"], int(row["age"])) for row in reader]

    conn.executemany(
        "INSERT INTO people (name, age) VALUES (?, ?)",
        rows
    )

def main():
    conn = sqlite3.connect("data.db")

    create_people_table(conn)
    conn.execute("DELETE FROM people")  # clear existing data so re-running this script doesn't duplicate rows
    load_people_csv(conn, "people.csv")

    conn.commit()
    conn.close()
    print("Database setup complete: data.db created with 'people' table loaded from people.csv")

if __name__ == "__main__":
    main()