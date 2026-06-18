import csv

people = [
    {"name": "Joshua", "age": 57},
    {"name": "Cici", "age": 45},
    {"name": "Matthew", "age": 12}
]

try:
    filename = "people.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerows(people)
        
except PermissionError:
    print(f"Permission Denied: You do not have rights to create '{filename}'.")

except FileExistsError:
    print(f"Naming Conflict: '{filename}' already exists.")

except FileNotFoundError:
    print("Path Error: One of the folders in your specified path does not exist.")

except ValueError as error:
    # Catches invalid modes or embedded null bytes in the filename string
    print(f"Invalid Argument: {error}")

except OSError as error:
    # Fallback block for all other system errors (locking, disk full, invalid chars)
    if error.errno == 22:  # EINVAL: Invalid argument (often bad characters on Windows)
        print(f"Bad Name: The filename '{filename}' contains invalid characters.")
    elif error.errno == 11 or error.errno == 35:  # EAGAIN / EDEADLK
        print(f"File Locking Error: The resource is locked by another process.")
    elif error.errno == 28:  # ENOSPC
        print("Disk Full: There is no space left on the device.")
    else:
        print(f"System Error ({error.errno}): {error.strerror}")