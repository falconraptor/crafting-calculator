import pickle
from argparse import ArgumentParser
from dataclasses import dataclass
from os.path import exists


class Recipe:
    inputs: list[tuple[str, int]]
    outputs: list[tuple[str, int]]  # < 1 is percent


@dataclass
class Item:
    name: str
    amount: int = 0


class Loader:
    __filename: str

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

    def main_menu(self):
        pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--recipes', metavar='FILE', default='recipes.dat')
    parser.add_argument('-i', '--inventory', metavar='FILE', default='inventory.dat')
    Crafter(**parser.__dict__).main_menu()
