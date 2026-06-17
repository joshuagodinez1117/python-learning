name1 ="Joshua"
name2 = "Cici"
name3 = "Matthew"

for i in range(1,4):
    if i == 1:
        print(f"{i}: {name1}")
    elif i == 2:
        print(f"{i}: {name2}")
    else:
        print(f"{i}: {name3}")

count = 1
while count <= 3:
    print(f"{count}:")
    print(count)
    count += 1