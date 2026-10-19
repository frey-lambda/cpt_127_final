import json


def config_refresh():
    global PERSON_TYPES, MENU_CHOICES, FEE
    with open('config.json', 'r') as file:
        python_list = json.load(file)
        PERSON_TYPES = python_list.get('person_types', [])
        MENU_CHOICES = python_list.get('menu_choices', [])
        FEE = python_list.get('fee', 0)

config_refresh()

def append_to_json(setting, value):
    config_refresh()
    with open('config.json', 'r+') as file:
        data = json.load(file)
        if setting == '1':
            data['person_types'].append(value)
        elif setting == '2':
            data['menu_choices'].append(value)
        else:
            print("Invalid setting. Use 1 for person_types or 2 for menu_choices.")
            return
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(f"Appended '{value}' to setting {setting}.")
    config_refresh()

def remove_from_json(setting, index):
    config_refresh()
    with open('config.json', 'r+') as file:
        data = json.load(file)
        if setting == '1':
            if 0 <= index < len(data['person_types']):
                removed_value = data['person_types'].pop(index)
            else:
                print("Invalid index for person_types.")
                return
        elif setting == '2':
            if 0 <= index < len(data['menu_choices']):
                removed_value = data['menu_choices'].pop(index)
            else:
                print("Invalid index for menu_choices.")
                return
        else:
            print("Invalid setting. Use 1 for person_types or 2 for menu_choices.")
            return
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(f"Removed '{removed_value}' from setting {setting}.")
    config_refresh()

def set_json_value(value):
    config_refresh()
    try:
        fee_value = int(value)
    except ValueError:
        print("Invalid value for fee. Please enter a numeric value.")
        return
    with open('config.json', 'r+') as file:
        data = json.load(file)
        data['fee'] = fee_value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(f"Set fee to {fee_value}.")
    config_refresh()

def expert_mode():
    print("Expert mode activated. 'help' for options.\n")
    while True:
        inp = input('>> ').lower()
        cmd_args = inp.split()
        cmd = cmd_args[0] if cmd_args else ''
        if cmd == 'exit':
            print('Exiting expert mode.')
            break
        if cmd == 'help':
            print("""
            Expert Mode is primarily used for changing the configuration file.
            In this mode, you can edit the config.json file directly. There are three settings you can change:
            1. person_types: A list of different types of people (e.g., member, guest).
            2. menu_choices: A list of available menu choices (e.g., chicken, beef, vegetarian).
            3. fee: The fee rate.\n
            COMMANDS: 
                append [setting] [value] - appends a value to either person_types or menu_choices. Use either 1 or 2 for [setting] as defined in the numbered list above.
                remove [setting] [index] - removes a value from either person_types or menu_choices at the specified index. Use either 1 or 2 for [setting] as defined in the numbered list above, as well as the index (based on 0) of the configuration value you want to remove.
                set [value] - sets the value (ONLY for setting 3) to the specified value.
                cnfg - prints the current configuration
                exit - exits expert mode""")
        if cmd == 'cnfg':
            print_config()
        if cmd == 'append':
            append_to_json(cmd_args[1], cmd_args[2])
        if cmd == 'remove':
            remove_from_json(cmd_args[1], int(cmd_args[2]))
        if cmd == 'set':
            set_json_value(cmd_args[1])

def print_config():
    config_refresh()
    print(f"Current Configuration:\nPerson Types: {PERSON_TYPES}\nMenu Choices: {MENU_CHOICES}\nFee: {FEE}")

config_refresh()