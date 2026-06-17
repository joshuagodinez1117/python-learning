person = {
    "name": "Joshua",
    "age": 57,
    "city": "Los Angeles"
}

print(person)

for key, value in person.items():
    print(f"{key}: {value}")

print("Adding phone number")

person["phone"] = "818-419-0108"

print(person)

for key, value in person.items():
    print(f"{key}: {value}")

print("Removing city")

del person["city"]

print(person)

for key, value in person.items():
    print(f"{key}: {value}")

