import json
from collections import defaultdict

ITEMS: dict[str, 'Item'] = {}


class Item:
    @classmethod
    def init(cls, name: str, recipes: list['Recipe'] = None) -> 'Item':
        if name in ITEMS:
            return ITEMS[name]
        if not recipes:
            recipes = []
        item = ITEMS[name] = Item(name, recipes)
        return item

    def __init__(self, name: str, recipes: list['Recipe'] = None):
        if not recipes:
            recipes = []
        self.name = name
        self.recipes = recipes

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self):
        return f'<Item name="{self.name}" num_recipes={len(self.recipes)}>'

    def get_best_route(self):
        routes: list[tuple[list[Recipe], dict[Item, float]]] = []
        to_process: list[list[Recipe]] = [[r] for r in self.recipes]
        for i, process in enumerate(to_process):
            while process:
                r = process.pop()
                if len(routes) == i:
                    routes.append(([r], defaultdict(int)))
                for item, a in r.inputs.items():
                    routes[i][1][item] = routes[i][1][item] + a
                    process.extend(item.recipes.copy())
        print('\n'.join(r.__repr__() for r in routes))


class Recipe:
    def __init__(self, inputs: dict[Item, float] = None, outputs: dict[Item, float] = None):
        if not inputs:
            inputs = {}
        self.inputs = inputs
        if not outputs:
            outputs = {}
        self.outputs = outputs
        for o in self.outputs:
            o.recipes.append(self)

    def __repr__(self) -> str:
        return f'<Recipe outputs={self.outputs!r} inputs={self.inputs!r}>'


if __name__ == '__main__':
    RECIPES = []
    with open('recipes.json', 'rt') as file:
        for obj in json.load(file):
            RECIPES.append(Recipe({Item.init(n): a for n, a in obj['inputs'].items()}, {Item.init(n): a for n, a in obj['outputs'].items()}))
    # print('\n'.join(_.__repr__() for _ in RECIPES))
    print(ITEMS['Reinforced Plate'].get_best_route())
