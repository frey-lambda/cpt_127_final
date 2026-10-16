import csv, xpert, datetime, json

MENU_CHOICES = xpert.MENU_CHOICES
PERSON_TYPES = xpert.PERSON_TYPES
FEE = xpert.FEE

def database_refresh():
    global DATABASE
    with open('bluff.csv', 'r') as file:
        reader = csv.reader(file)
        DATABASE = list(reader)

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
    for entry in DATABASE:
        for cell in entry:
            print(f'{cell:<25}', end='')
        print()

def new_entry():
    database_refresh()

def edit_entry():
    database_refresh()

def delete_entry(entry_id):
    database_refresh()

def search_entries(query):
    database_refresh()

def report_chooser():
    database_refresh()

def backup_entries():
    database_refresh()

def boilerplate(cmd_args):
    cmd = cmd_args[0] if cmd_args else ''
    if cmd == 'help':
        print_help()
    if cmd == 'list':
        list_entries()
    if cmd == 'new':
        new_entry()
    if cmd == 'edit':
        edit_entry()
    if cmd == 'del':
        delete_entry(cmd_args[1] if len(cmd_args) > 1 else None)
    if cmd == 'src':
        search_entries(cmd_args[1] if len(cmd_args) > 1 else None)
    if cmd == 'rprt':
        report_chooser()
    if cmd == 'bckp':
        backup_entries()
    if cmd == 'xpert':
        xpert.expert_mode()
    if cmd == 'cnfg':
        xpert.print_config()

def main():
    xpert.config_refresh()
    while True:
        cmd = input('> ').lower()
        if cmd == 'exit':
            print('Goodbye.')
            break
        boilerplate(cmd.split())

main()