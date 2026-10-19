import random, csv, json, xpert

MENU_CHOICES = xpert.MENU_CHOICES
PERSON_TYPES = xpert.PERSON_TYPES
FEE = xpert.FEE

xpert.config_refresh()

def name_gen():
    with open('names.txt', 'r') as file:
        names = [line.strip() for line in file]
    first_name_index = random.randint(0, len(names) - 1)
    while True:
        last_name_index = random.randint(0, len(names) - 1)
        if last_name_index != first_name_index:
            break
    return f"{names[first_name_index]} {names[last_name_index]}"

def generate_data(entry_num):
    with open('bluff.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Category", "Food Choice", "Fee amount received", "Fee Paid?"])
        for i in range(1, entry_num + 1):
            fee_is_paid = random.choice([True, False])
            to_write = [name_gen(), random.choice(PERSON_TYPES), random.choice(MENU_CHOICES), FEE if fee_is_paid else random.randint(1, int(FEE)), fee_is_paid]
            writer.writerow(to_write)

if __name__ == "__main__":
    generate_data(1000)