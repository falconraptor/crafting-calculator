import json


def display_commands(command_list):
    print()
    for i, e in enumerate(command_list):
        print('{}) {}'.format(i + 1, e))


def get_menu_item(command_list):
    i = -1
    while i < 0 or i > len(command_list):
        display_commands(command_list)
        i = int(input('What would you like to do? '))
        if 0 < i <= len(command_list):
            return i - 1


def load(recipes='recipes.json', inventory='inv.json'):
    try:
        with open(recipes) as fp:
            recipe = json.load(fp)
    except FileNotFoundError:
        recipe = {}
    try:
        with open(inventory) as fp:
            inv = json.load(fp)
    except FileNotFoundError:
        inv = {}
    return inv, recipe


def save(recipes='recipes.json', inventory='inv.json', inv=None, recipe=None):
    with open(recipes, 'w') as fp:
        json.dump(recipe or {}, fp, sort_keys=True, indent=4)
    with open(inventory, 'w') as fp:
        json.dump(inv or {}, fp, sort_keys=True, indent=4)


def inventory(inv=None):
    if inv is None:
        inv = {}
    commands = ['Add', 'Remove', 'View', 'Clear', 'Back']
    while True:
        command = commands[get_menu_item(commands)].lower()
        print()
        if command == 'back':
            return inv
        elif command == 'add':
            name = input('What item would you like to add to your inventory? ').lower()
            amount = int(input('What amount of {} would you like to add your inventory? '.format(name)))
            try:
                inv[name] += amount
            except KeyError:
                inv[name] = amount
            print('Added {} of {} to your inventory'.format(amount, name))
        elif command == 'view':
            for name, amount in inv.items():
                print('{}: {}'.format(name, amount))
        elif command == 'remove':
            keys = list(inv)
            for index, name in enumerate(keys):
                print('{}) {}'.format(index + 1, name))
            item = int(input('\nWhat item would you like to remove from your inventory? ') or -1) - 1
            if item < 0 or item > len(keys):
                continue
            amount = int(input('How much of {} would you like to remove from your inventory [{}]? '.format(keys[item], inv[keys[item]])))
            if amount == inv[keys[item]]:
                del inv[keys[item]]
            else:
                inv[keys[item]] -= amount
                if inv[keys[item]] < 0:
                    del inv[keys[item]]
            print('Removed {} of {} from your inventory'.format(amount, keys[item]))
        elif command == 'clear':
            inv.clear()
            print('Inventory cleared')


def craft(inv=None, recipe=None):
    if inv is None:
        inv = {}
    if recipe is None:
        recipe = {}
    commands = ['List recipes', 'Craft Item', 'Back']
    while True:
        command = commands[get_menu_item(commands)].lower()
        print()
        if command == 'back':
            return inv, recipe
        elif command == 'list recipes':
            pass
        elif command == 'craft item':
            pass


def recipes(inv=None, recipe=None):
    if inv is None:
        inv = {}
    if recipe is None:
        recipe = {}
    commands = ['Add', 'Remove', 'Edit', 'View', 'Clear', 'Back']
    while True:
        command = commands[get_menu_item(commands)].lower()
        print()
        if command == 'back':
            return inv, recipe
        elif command == 'view':
            for item, obj in recipe.items():
                print('{} makes {} using:'.format(item, obj['amount']))
                for item, amount in obj['requires'].items():
                    print('  - {} of {}'.format(amount, item))
                print()
        elif command == 'remove':
            keys = list(inv)
            for index, name in enumerate(keys):
                print('{}) {}'.format(index + 1, name))
            item = int(input('\nWhat recipe would you like to remove? ') or -1) - 1
            if item < 0 or item > len(keys):
                continue
            del recipe[keys[item]]
            print('Removed recipe for ' + keys[item])
        elif command == 'edit':
            keys = list(recipe)
            for index, name in enumerate(keys):
                print('{}) {}'.format(index + 1, name))
            print()
            item = int(input('What recipe would you like to edit [-1]? ') or -1) - 1
            if item < 0 or item > len(keys):
                continue
            name = input('What is the new item this recipe makes [{}]? '.format(keys[item])) or keys[item]
            if name != keys[item]:
                recipe[name] = dict(recipe[keys[item]])
                del recipe[keys[item]]
            r = recipe[name]
            r['amount'] = int(input('What is the new amount of {} that this recipe makes [{}]? '.format(name, r['amount']))) or r['amount']
            done = input('Would you like to edit the items required for this recipe (y/n) [n]? ').lower().strip() == 'y'
            while done:
                keys = list(r['requires'])
                for index, name in enumerate(keys):
                    print('{}) {} of {}'.format(index + 1, r['requires'][keys[index]], name))
                item = int(input('\nWhat item would you like to edit [-1]? ') or -1) - 1
                if len(keys) > item >= 0:
                    sub_commands = ['Change Item', 'Change Amount', 'Remove Item', 'Back']
                    command = sub_commands[get_menu_item(sub_commands)].lower()
                    if command == 'change item':
                        new_item = input('What is the name of the item that you would like to replace this item with [{}]? '.format(keys[item])) or keys[item]
                        if new_item != keys[item]:
                            r['requires'][new_item] = r['requires'][keys[item]]
                            print('{} of {} changed to {} of {}'.format(r['requires'][keys[item]], keys[item], r['requires'][keys[item]], new_item))
                    elif command == 'change amount':
                        new_amount = input('What is the new amount of {} that this item requires [{}]? '.format(keys[item], r['requires'][keys[item]]))
                        if r['requires'][keys[item]] != new_amount:
                            r['requires'][keys[item]] = new_amount
                            print('{} of {} changed to {} of {}'.format(r['requires'][keys[item]], keys[item], r['requires'][keys[item]], keys[item]))
                    elif command == 'remove item':
                        del r['requires'][keys[item]]
                        print(keys[item] + ' removed from recipe')
                done = input('Would you like to edit another item required for this recipe (y/n) [n]? ').lower().strip() == 'y'
        elif command == 'clear':
            recipe.clear()
            print('Clear complete!')
        elif command == 'add':
            name = input('What recipe would you like to add? ').lower()
            if name in recipe:
                print('That recipe already exists!')
                continue
            amount = int(input('What amount of {} does this recipe make [1]? '.format(name)) or 1)
            recipe[name] = {'amount': amount, 'requires': {}}
            while True:
                item = input('What item does this recipe require or "done"? ').lower() or 'done'
                if item == 'done':
                    break
                recipe[name]['requires'][item] = int(input('What amount of {} does this recipe require [1]? '.format(item)) or 1)
            print('Added recipe for ' + name)


def main():
    commands = ['Craft', 'Inventory', 'Load', 'Save', 'Recipes', 'Quit']
    inv = {}
    recipe = {}
    while True:
        command = commands[get_menu_item(commands)].lower()
        print()
        if command == 'quit':
            return
        elif command in {'save', 'load'}:
            recipe_file = input('What file would you like to {} the recipes from [recipes.json]? '.format(command)) or 'recipes.json'
            inventory_file = input('What file would you like to {} your inventory from [inv.json]? '.format(command)) or 'inv.json'
            if command == 'save':
                save(recipe_file, inventory_file, inv, recipe)
            else:
                inv, recipe = load(recipe_file, inventory_file)
            print('{} successful'.format(command))
        elif command in {'inventory', 'craft', 'recipes'}:
            if command == 'inventory':
                inv = globals()[command](inv)
            else:
                inv, recipe = globals()[command](inv, recipe)


if __name__ == '__main__':
    main()
