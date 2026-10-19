import csv, xpert, datetime, json, shutil, datetime

MENU_CHOICES = xpert.MENU_CHOICES
PERSON_TYPES = xpert.PERSON_TYPES
FEE = xpert.FEE
DATABASE = []

def gather_name():
        input_name = input("Name: ")
        if input_name.lower() in [entry[0].lower() for entry in DATABASE]:
            print("Entry already exists.")
            return gather_name()
        if input_name == '':
            print("Name cannot be empty.")
            return gather_name()
        if input_name.lower() == 'exit':
            print("Exiting entry creation.")
            return None
        return input_name

def gather_person_type():
    person_type = input(f"Person Type: ")
    if person_type.lower() not in [person_type.lower() for person_type in PERSON_TYPES] and person_type.lower() != 'list' and person_type.lower() != 'exit':
        print(f"Invalid person type.")
        return gather_person_type()
    elif person_type.lower() == 'list':
        print(f"Available person types: {', '.join(PERSON_TYPES)}")
        return gather_person_type()
    elif person_type.lower() == 'exit':
        print("Exiting entry creation.")
        return None
    return person_type
    
def gather_menu_choice():
    menu_choice = input(f"Food Choice: ")
    if menu_choice.lower() not in [menu_choice.lower() for menu_choice in MENU_CHOICES] and menu_choice.lower() != 'list' and menu_choice.lower() != 'exit':
        print(f"Invalid menu choice.")
        return gather_menu_choice()
    if menu_choice.lower() == 'list':
        print(f"Available menu choices: {', '.join(MENU_CHOICES)}")
        return gather_menu_choice()
    if menu_choice.lower() == 'exit':
        print("Exiting entry creation.")
        return None
    return menu_choice
    
def gather_fee_amount_procured():
    fee_amount = input(f"Fee amount received: ")
    if not fee_amount.isdigit():
        print("Invalid fee amount. Please enter a numeric value.")
        return gather_fee_amount_procured()
    if int(fee_amount) > FEE:
        print(f"Fee amount cannot exceed {FEE}.")
        return gather_fee_amount_procured()
    if int(fee_amount) < 0:
        print("Fee amount cannot be negative.")
        return gather_fee_amount_procured()
    return int(fee_amount)

def database_refresh():
    global DATABASE
    with open('bluff.csv', 'r') as file:
        reader = csv.reader(file)
        DATABASE = list(reader)

def formatter(entries):
    for entry in entries:
        for cell in entry:
            print(f'{cell:<25}', end='')
        print()

def print_help():
    print("""
    Welcome to the Help Menu. Here are the available commands:
    help - Displays this help menu.
    list - Lists all entries in the database.
    new - Creates a new entry in the database.
    edit [entry_id] - Edits an existing entry with the specified entry_id.
    del [entry_id] - Deletes an entry with the specified entry_id.
    src [query] - Searches for entries matching the query.
    rprt - Chooses a report to generate.
    bckp - Backs up the database.
    xpert - Enters expert mode for advanced configuration.
    cnfg - Displays the current configuration settings.
    exit - Exits the program.""")

def list_entries():
    database_refresh()
    if not DATABASE:
        print("No entries found in the database.")
        return
    print("Listing all entries:")
    formatter(DATABASE)

def new_entry():
    database_refresh()
    input_name = gather_name()
    if input_name is None:
        return

    person_type = gather_person_type()
    if person_type is None:
        return

    menu_choice = gather_menu_choice()
    if menu_choice is None:
        return

    fee_paid_input = input(f"Is the fee paid? (y/N): ")
    if fee_paid_input.lower() == 'y':
        fee_paid = True
        fee_amount = FEE
    
    else:
        fee_paid = False
        fee_amount = gather_fee_amount_procured()
        if fee_amount is None:
            return
    
    print(f"Writing...")    
    with open('bluff.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([input_name, person_type, menu_choice, fee_amount, fee_paid])
    print(f"Done! Entry for {input_name} at index {len(DATABASE)} has been added to the database.")

def edit_entry(entry_id):
    database_refresh()
    if entry_id is None or not entry_id.isdigit() or int(entry_id) < 0 or int(entry_id) >= len(DATABASE):
        print("Invalid entry ID.")
        return
    else:
        entry_id = int(entry_id)
    entry = DATABASE[entry_id]
    print(f"Editing entry: {entry}")
    print("Enter 1 for Name, 2 for Person Type, 3 for Food Choice, 4 for Fee amount received: ")
    field_choice = input("Field to edit: ")
    if field_choice == '1':
        gathered_name = gather_name()
        if gathered_name is None:
            return
        DATABASE[entry_id][0] = gathered_name
        entry[0] = gathered_name
    elif field_choice == '2':
        gathered_person_type = gather_person_type()
        if gathered_person_type is None:
            return
        entry[1] = gathered_person_type
    elif field_choice == '3':
        gathered_menu_choice = gather_menu_choice()
        if gathered_menu_choice is None:
            return
        entry[2] = gathered_menu_choice
    elif field_choice == '4':
        gathered_fee_amount = gather_fee_amount_procured()
        if gathered_fee_amount is None:
            return
        entry[3] = gathered_fee_amount
        if gathered_fee_amount == FEE:
            entry[4] = True
        else:
            entry[4] = False
    else:
        print("Invalid field choice.")
        return
    with open('bluff.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(DATABASE)

def delete_entry(entry_id):
    database_refresh()
    if entry_id is None or not entry_id.isdigit() or int(entry_id) < 0 or int(entry_id) >= len(DATABASE):
        print("Invalid entry ID.")
        return
    else:
        entry_id = int(entry_id)
    entry = DATABASE[entry_id]
    confirmation = input(f"Are you sure you want to delete the entry for {entry[0]}? (y/N): ")
    if confirmation.lower() == 'y':
        DATABASE.pop(entry_id)
        with open('bluff.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(DATABASE)
        print(f"Entry for {entry[0]} has been deleted.")

def search_entries(name):
    database_refresh()
    if name is None:
        print("Please provide a name to search for.")
        return
    found_entry = False
    for entry in DATABASE:
        if name.lower() in entry[0].lower():
            print(f"Found entry: {entry} at index {DATABASE.index(entry)}")
            found_entry = True
    if not found_entry:
        print(f"No entries found for {name}.")
        return False
    return found_entry

def report_chooser(option=None):
    database_refresh()
    if option is None:
        print("Choose a report to generate:")
        print("1. List all entries")
        print("2. List all entries with fee paid")
        print("3. List all entries with fee not paid")
        print("4. List all entries with a specific person type")
        print("5. List all entries with a specific food choice")

        report_choice = input("Report choice: ")
    else:
        report_choice = option
    reported = []
    if report_choice == '1':
        reported = DATABASE
    elif report_choice == '2':
        print("Entries with fee paid:")
        for entry in DATABASE:
            if entry[4].lower() == 'true':
                reported.append(entry)
    elif report_choice == '3':
        print("Entries with fee not paid:")
        for entry in DATABASE:
            if entry[4].lower() == 'false':
                reported.append(entry)
    elif report_choice == '4':
        person_type = input("Enter person type: ")
        print(f"Entries with person type '{person_type}':")
        for entry in DATABASE:
            if entry[1].lower() == person_type.lower():
                reported.append(entry)
    elif report_choice == '5':
        food_choice = input("Enter food choice: ")
        print(f"Entries with food choice '{food_choice}':")
        for entry in DATABASE:
            if entry[2].lower() == food_choice.lower():
                reported.append(entry)
    formatter(reported)
    backup_response =input("Make backup of this report? (y/N): ")
    if backup_response.lower() == 'y':
        with open(f'Reports/report_{report_choice}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(reported)
        print("Report backed up successfully.")

def backup_entries():
    shutil.copy('bluff.csv', f'Backups/data_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

def restore_backup(id):
    shutil.copy(f'Backups/data_backup_{id}.csv', 'bluff.csv')
    database_refresh()

def boilerplate(cmd_args):
    cmd = cmd_args[0] if cmd_args else ''
    if cmd == 'help':
        print_help()
    elif cmd == 'list':
        list_entries()
    elif cmd == 'new':
        new_entry()
    elif cmd == 'edit':
        edit_entry(cmd_args[1] if len(cmd_args) > 1 else None)
    elif cmd == 'del':
        delete_entry(cmd_args[1] if len(cmd_args) > 1 else None)
    elif cmd == 'src':
        search_entries(cmd_args[1] if len(cmd_args) > 1 else None)
    elif cmd == 'rprt':
        report_chooser(cmd_args[1] if len(cmd_args) > 1 else None)
    elif cmd == 'bckp':
        backup_entries()
    elif cmd == 'xpert':
        xpert.expert_mode()
    elif cmd == 'cnfg':
        xpert.print_config()
    elif cmd == 'rstr':
        restore_backup(cmd_args[1] if len(cmd_args) > 1 else None)
    else:
        print("Invalid command. Type 'help' for a list of commands.")

def main():
    xpert.config_refresh()
    while True:
        cmd = input('> ').lower()
        if cmd == 'exit':
            print('Goodbye.')
            break
        boilerplate(cmd.split())

if __name__ == "__main__":
    main()