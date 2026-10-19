length = 0

with open('names.txt', 'r') as file:
        names = [line.strip() for line in file]
        for name in names:
            if len(name) > length:
                length = len(name)
        print(f"Longest name length: {length}")