from report import summarize

import csv

def load_people_csv(filename):
    rows=[]
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["age"] = int(row["age"])
                    rows.append(row)
                except ValueError:
                    print(f"Skipping {row['name']}: invalid age value '{row['age']}'")
            
    except PermissionError:
        print(f"Permission Denied: You do not have rights to open '{filename}'.")

    except FileNotFoundError:
        print("File Not Found Error: The path or filename  does not exist.")

    except ValueError as error:
        # Catches invalid modes or embedded null bytes in the filename string
        print(f"Invalid Argument trying to open file: {error}")

    except OSError as error:
        # Fallback block for all other system errors (locking, disk full, invalid chars)
        if error.errno == 22:  # EINVAL: Invalid argument (often bad characters on Windows)
            print(f"Bad Name: The filename '{filename}' contains invalid characters.")
        elif error.errno == 11 or error.errno == 35:  # EAGAIN / EDEADLK
            print(f"File Locking Error: The resource is locked by another process.")
        else:
            print(f"System Error ({error.errno}): {error.strerror}")
    return rows

def load_multiple(filenames):
    all_people = []
    for filename in filenames:
        people = load_people_csv(filename)
        all_people.extend(people)
    return all_people

#rows = load_people_csv("people.csv")

#for row in rows:
#    print(f"{row['name']} is {row['age']} years old!")

#summarize(rows)

everyone = load_multiple(["people.csv", "people.csv"])
print(f"\nCombined load result: {len(everyone)} total records")
summarize(everyone)