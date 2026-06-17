person = {
    "name": "Joshua",
    "age": 57,
    "city": "Los Angeles",
    "phone": "818-419-0108"
}

people = [

    {"name": "Cici", "age": 45, "city": "Burbank"},

    {"name": "Matthew", "age": 30, "city": "Glendale"}

]

people.append(person)

for person in people:
    print(f"{person.get('name', 'Name is null')}, Phone: {person.get('phone', 'Phone is null')}")