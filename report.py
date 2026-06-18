def summarize(people):
    if not people:
        print("No people to summarize.")
        return

    total = len(people)
    average_age = sum(p["age"] for p in people) / total
    oldest = max(people, key=lambda p: p["age"])
    youngest = min(people, key=lambda p: p["age"])

    print(f"Total people: {total}")
    print(f"Average age: {average_age:.1f}")
    print(f"Oldest: {oldest['name']} ({oldest['age']})")
    print(f"Youngest: {youngest['name']} ({youngest['age']})")