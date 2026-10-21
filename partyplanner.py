import csv, xpert, datetime, json, shutil, datetime, bluff_data_gen

MENU_CHOICES = xpert.MENU_CHOICES
PERSON_TYPES = xpert.PERSON_TYPES
FEE = xpert.FEE
DATABASE = []

def gather_name():
        #take input for name
        input_name = input("Name: ")

        #check if in database
        if input_name.lower() in [entry[0].lower() for entry in DATABASE]:
            print("Entry already exists.")
            #recursively call again
            return gather_name()
        
        #check if name is empty
        if input_name == '':
            print("Name cannot be empty.")
            #recursively call again
            return gather_name()
        if input_name.lower() == 'exit':
            #exit the entry creation
            print("Exiting entry creation.")
            return None
        #return name when valid
        return input_name

def gather_person_type():
    #take input for person type
    person_type = input(f"Person Type: ")

    #check if person type is within the list of person types
    if person_type.lower() not in [person_type.lower() for person_type in PERSON_TYPES] and person_type.lower() != 'list' and person_type.lower() != 'exit':
        print(f"Invalid person type.")
        return gather_person_type()

    #print a list of all person types and recursively call again
    elif person_type.lower() == 'list':
        print(f"Available person types: {', '.join(PERSON_TYPES)}")
        return gather_person_type()
    
    #exit the entry creation
    elif person_type.lower() == 'exit':
        print("Exiting entry creation.")
        return None
    #return person type when valid
    return person_type
    
def gather_menu_choice():
    #take input for menu choice
    menu_choice = input(f"Food Choice: ")
    #check if menu choice is within the list of menu choices
    if menu_choice.lower() not in [menu_choice.lower() for menu_choice in MENU_CHOICES] and menu_choice.lower() != 'list' and menu_choice.lower() != 'exit':
        print(f"Invalid menu choice.")
        return gather_menu_choice()
    #print a list of all menu choices and recursively call again
    if menu_choice.lower() == 'list':
        print(f"Available menu choices: {', '.join(MENU_CHOICES)}")
        return gather_menu_choice()
    #exit the entry creation
    if menu_choice.lower() == 'exit':
        print("Exiting entry creation.")
        return None
    return menu_choice
    
def gather_fee_amount_procured():
    #take input for fee amount procured
    fee_amount = input(f"Fee amount received: ")
    if not fee_amount.isdigit():
        print("Invalid fee amount. Please enter a numeric value.")
        return gather_fee_amount_procured()
    #check if fee amount is greater than FEE or negative and recursively call again if so
    if int(fee_amount) > FEE:
        print(f"Fee amount cannot exceed {FEE}.")
        return gather_fee_amount_procured()
    if int(fee_amount) < 0:
        print("Fee amount cannot be negative.")
        return gather_fee_amount_procured()
    return int(fee_amount)

def database_refresh():
    #refresh the database by reading from partyplanner.csv and reinitializing the DATABASE variable
    global DATABASE
    with open('partyplanner.csv', 'r') as file:
        reader = csv.reader(file)
        DATABASE = list(reader)

def formatter(entries):
    #format all entries in the database to be printed in a table format
    if not entries:
        raise ValueError("No entries to format.")
    for entry in entries:
        for cell in entry:
            print(f'{cell:<25}', end='')
        print()

def print_help():
    #prints help menu
    print("""
    Welcome to the Help Menu. Here are the available commands:
    help - Displays this help menu.
    list - Lists all entries in the database.
    new - Creates a new entry in the database.
    edit [entry_id] - Edits an existing entry with the specified entry_id.
    del [entry_id] - Deletes an entry with the specified entry_id.
    src [query] - Searches for entries matching the query.
    rprt [report_id (optional)] - Chooses a report to generate. If report_id is provided, it generates that specific report. If not, it prompts for a report choice.
    bckp - Backs up the database.
    rstr [backup_id] - Restores the database from a backup with the specified backup_id.
    gen [entry_num] - Generates a specified number of random entries in the database. If no number is provided, it defaults to 1000 entries.
    stats - Generates statistics about the database and saves a report to Stats folder.
    xpert - Enters expert mode for advanced configuration.
    cnfg - Displays the current configuration settings.
    exit - Exits the program.""")

def list_entries():
    #refresh the database and print all entries in a formatted table
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
    with open('partyplanner.csv', 'a', newline='') as file:
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
    with open('partyplanner.csv', 'w', newline='') as file:
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
        with open('partyplanner.csv', 'w', newline='') as file:
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
    #backup the database by copying partyplanner.csv to Backups folder with timestamp
    print(f"Backing up database to Backups/data_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    shutil.copy('partyplanner.csv', f'Backups/data_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    print("Backup completed successfully. Id for this backup is: " + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

def restore_backup(id):
    #restore the database by copying the backup file to partyplanner.csv and refreshing the database
    if id is None:
        print("Please provide a backup ID to restore.")
        return
    if not shutil.os.path.exists(f'Backups/data_backup_{id}.csv'):
        print(f"No backup found with ID {id}.")
        return
    print(f"Restoring backup with ID {id}...")
    shutil.copy(f'Backups/data_backup_{id}.csv', 'partyplanner.csv')
    database_refresh()
    print(f"Backup with ID {id} restored successfully.")

def count_each_item(item_list):
    #checks through a list and counts how many times each item appears in the list, returning a dictionary with the item as the key and the count as the value
    product_count = {}
    for item in item_list:
        if item not in product_count:
            product_count[item] = 1
        else:
            product_count[item] += 1
    return product_count

def format_dictionary(dictionary):
    for key, value in dictionary.items():
        print(f"{key:<25}: {value:<25}")

def generate_statistics():
    database_refresh()

    #remove the header row from the database
    DATABASE.pop(0)

    #retrieve all chosen menu items and person types from the database
    all_chosen_menu_items = [entry[2] for entry in DATABASE]
    all_chosen_person_types = [entry[1] for entry in DATABASE]

    #initialize dicts
    menu_item_counts = {}
    person_type_counts = {}

    #make sure each menu item is in config.json
    for chosen_menu_item in all_chosen_menu_items:
        if chosen_menu_item not in MENU_CHOICES:
            print("It seems as though the config.json file is not set up properly. Please fix either database.csv or config.json\nPlease note that running the gen command will refresh the database with working files as long as config.json is still correctly formatted.")
            break
    
    #count how many times each menu item and person type appears in the database
    menu_item_counts = count_each_item(all_chosen_menu_items)
    menu_item_amount = len(menu_item_counts)
    
    for chosen_person_type in all_chosen_person_types:
        if chosen_person_type not in PERSON_TYPES:
            print("It seems as though the config.json file is not set up properly. Please fix either database.csv or config.json\nPlease note that running the gen command will refresh the database with working files as long as config.json is still correctly formatted.")
            break
        person_type_counts = count_each_item(all_chosen_person_types)
        person_type_amount = len(person_type_counts)
    
    #initialize fee paid count and amount procured total
    fee_paid_count = 0
    for entry in DATABASE:
        entry = entry[4]
        if entry == "True": #string comparison because the CSV stores booleans as strings
            fee_paid_count += 1
    amount_procured_total = 0
    for entry in DATABASE:
        amount_procured_total += int(entry[3])
    
    entry_count = len(DATABASE)
    
    print("Menu Choices")
    format_dictionary(menu_item_counts)
    print(f"There are {menu_item_amount} different menu choices in the database")
    print()
    print("Person Types")
    format_dictionary(person_type_counts)
    print(f"There are {person_type_amount} different person types in the database")
    print()
    print(f"So far, {fee_paid_count} people have paid the full fee")
    print(f"So far, ${amount_procured_total} has been procured")
    print()
    print(f"There are {entry_count} entries")
    print()
    print(f"Saving report to Stats/statistics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(f"Stats/statistics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
        f.write("Menu Choices\n")
        for key, value in menu_item_counts.items():
            f.write(f"{key:<25}: {value:<25}\n")
        f.write(f"There are {menu_item_amount} different menu choices in the database\n\n")
        f.write("Person Types\n")
        for key, value in person_type_counts.items():
            f.write(f"{key:<25}: {value:<25}\n")
        f.write(f"There are {person_type_amount} different person types in the database\n\n")
        f.write(f"So far, {fee_paid_count} people have paid the full fee\n")
        f.write(f"So far, ${amount_procured_total} has been procured\n\n")
        f.write(f"There are {entry_count} entries\n")
    print(f"Report saved to Stats/statistics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    print("Done!")

def fix_csv():
    #fixes the partyplanner.csv file by generating a new one with test data
    option = input("There are two options immediately: 1. Generate with test data. 2. Restore from backup.\nType 1 or 2 to choose. Press enter to continue. > ")
    if option == '1':
        entry_num = input("How many entries to generate? (Press enter for default 1000 entries. If entry is invalid, we will default to 1000 entries.) > ")
        bluff_data_gen.generate_data(int(entry_num) if entry_num.isdigit() else 1000)
    elif option == '2':
        id = input("Enter the backup ID to restore from. (Press enter to continue) > ")
        restore_backup(id)

def csv_validation():
    #check if partyplanner.csv exists and is valid
    try:
        with open('partyplanner.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 5:
                    print("Invalid CSV format. Each row must have 5 columns.")
                    if input("Run fixes? (y/N): ").lower() == 'y':
                        fix_csv()
                    else:
                        print("Exiting due to invalid CSV format.")
                        exit(1)
    except FileNotFoundError:
        fix = input("partyplanner.csv not found. Run fixes? (y/N): ")
        if fix.lower() == 'y':
            fix_csv()
        else:
            print("Exiting due to missing CSV file.")
            exit(1)

def boilerplate(cmd_args):
    database_refresh()
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
    elif cmd == 'gen':
        bluff_data_gen.generate_data(int(cmd_args[1]) if len(cmd_args) > 1 and cmd_args[1].isdigit() else 1000)
    elif cmd == 'stats':
        generate_statistics()
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
    csv_validation()
    main()