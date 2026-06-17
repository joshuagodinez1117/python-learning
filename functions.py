names = ["Joshua", "Cici", "Matthew"]

def check_name(namesearch):
    for name in names:
        print(namesearch, name)
        if name == namesearch:
            return True
        
    return False

print(check_name("Joshua"))
print(check_name("Bob"))
