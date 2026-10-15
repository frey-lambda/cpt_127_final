def initialize():
    print('Welcome to the Guest Manager!')
    print('Type "help" for a list of commands.')
    

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