import random, csv

FEE = 25
bluff_data = []

with open('bluff.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        bluff_data.append(row[0])

choose_list = ["member", "guest", "volunteer", "staff", "sponsor", "vip"]
menu_list = ["chicken", "beef", "vegetarian", "vegan", "gluten-free"]

for i in range(1,1000):
    fee_is_paid = random.choice([True, False])
    to_write = [bluff_data[i], random.choice(choose_list), random.choice(menu_list), 25 if fee_is_paid else random.randint(1, 25), fee_is_paid]
    print(f'{to_write[0]}, {to_write[1]}, {to_write[2]}, {to_write[3]}, {to_write[4]}')