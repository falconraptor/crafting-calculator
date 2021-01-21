import pickle
from argparse import ArgumentParser
from dataclasses import dataclass
from os.path import exists


class Recipe:
    inputs: list[tuple[str, int]]
    outputs: list[tuple[str, int]]  # < 1 is percent chance


@dataclass
class Item:
    name: str
    amount: int = 0

    def __add__(self, other: int):
        self.amount += other

    def __sub__(self, other: int):
        self.amount -= other


class Loader:
    __filename: str
    __autosave: bool = True

    @classmethod
    def load(cls, filename):
        if exists(filename):
            with open(filename, 'rb') as file:
                instance = pickle.load(file)
        else:
            instance = cls()
        instance.__filename = filename
        return instance

    def save(self, filename: str = ''):
        with open(filename or self.__filename, 'wb') as file:
            pickle.dump(self, file)

    def __del__(self):
        if self.__autosave and self.__filename:
            self.save()


class Commands:
    @classmethod
    def int_select(cls, commands: list[str]) -> str:
        print('Please select by inputting the number:')
        for i, command in enumerate(commands):
            print(f'{i + 1}) {command}')
        len_commands = len(commands)
        while True:
            user = input('? ')
            try:
                user = int(user)
                if user < 1 or user > len_commands:
                    raise ValueError
                return commands[user]
            except ValueError:
                print('Not a valid number')


class Inventory(Loader):
    __items: dict[str, Item] = {}

    def get_item(self, item: str) -> Item:
        obj = self.__items.get(item)
        if not obj:
            obj = self.__items[item] = Item(item)
        return obj


class RecipeManager(Loader):
    __recipes: list[Recipe] = []

    def get_recipes(self, item: str) -> list[Recipe]:
        return [recipe for recipe in self.__recipes for output in recipe.outputs if output[0] == item]

    def get_usage(self, item: str) -> list[Recipe]:
        return [recipe for recipe in self.__recipes for input in recipe.inputs if input[0] == item]


class Crafter:
    def __init__(self, recipes: str = 'recipes.dat', inventory: str = 'inventory.dat'):
        self.inventory = Inventory.load(inventory)
        self.recipes = RecipeManager.load(recipes)
        self.main_menu()

    def main_menu(self):
        while True:
            select = Commands.int_select(['Manage Inventory', 'Manage Recipes', 'Craft', 'Exit'])
            if select == 'Manage Inventory':
                self.inventory.manage()
            elif select == 'Manage Recipes':
                self.recipes.manage()
            elif select == 'Craft':
                self.craft()
            elif select == 'Exit':
                break

    def craft(self):
        pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--recipes', metavar='FILE', default='recipes.dat')
    parser.add_argument('-i', '--inventory', metavar='FILE', default='inventory.dat')
    Crafter(**parser.__dict__).main_menu()
