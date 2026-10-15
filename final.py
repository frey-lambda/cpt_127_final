import json, csv

PERSON_TYPES = []
MENU_CHOICES = []
FEE = 0

def print_help():
    pass

def list_entries():
    pass

def new_entry():
    pass

def edit_entry():
    pass

def delete_entry(entry_id):
    pass

def search_entries(query):
    pass

def report_chooser():
    pass

def backup_entries():
    pass

def expert_mode():
    pass

def print_config():
    pass

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
        expert_mode()
    if cmd == 'cnfg':
        print_config()

def main():
    initialize()
    while True:
        cmd = input('> ').lower()
        if cmd == 'exit':
            print('Goodbye.')
            break
        boilerplate(cmd.split())

with open('config.json', 'r') as file:
    python_list = json.load(file)

print(python_list)