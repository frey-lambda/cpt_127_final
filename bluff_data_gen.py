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

with open('bluff.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Category", "Food Choice", "Fee amount received", "Fee Paid?"])
    for i in range(1, 1000):
        fee_is_paid = random.choice([True, False])
        to_write = [name_gen(), random.choice(PERSON_TYPES), random.choice(MENU_CHOICES), FEE if fee_is_paid else random.randint(1, int(FEE)), fee_is_paid]
        writer.writerow(to_write)

# for i in range(1,1000):
#    fee_is_paid = random.choice([True, False])
#    to_write = [name_gen(), random.choice(choose_list), random.choice(menu_list), FEE if fee_is_paid else random.randint(1, FEE), fee_is_paid]
#    print(f'{to_write[0]}, {to_write[1]}, {to_write[2]}, {to_write[3]}, {to_write[4]}')