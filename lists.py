names = ["Joshua", "Cici", "Matthew"]

for i, name in enumerate(names):
    print(f"{i}: {name}")

print(names)

print(f"\n{names[0]} should be Joshua")

for name in names:
    print(name, id(name))

print("names[0] id:", id(names[0]))