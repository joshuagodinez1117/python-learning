names = ["Joshua", "Cici", "Matthew"]

def save_names(names, filename):
    with open(filename, "w") as file:
        for name in names:
            file.write(name + "\n")

save_names(names, "names.txt")

def load_names(filename):
    with open(filename, "r") as file:
        loaded_names = [line.strip() for line in file]

    return loaded_names


print(load_names("names.txt"))
