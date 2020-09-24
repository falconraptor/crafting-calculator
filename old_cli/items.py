import json


class Crafter:
    def __init__(self):
        self.raw = {}
        self.excess = {}

    def get_requires(self, item, all_items, clear=True):
        """
        :param clear: 
        :param item: JSON obj / PY dict of 1 item 
        :param all_items: JSON obj / PY dict of all items 
        """
        if clear:
            self.raw = {}
            self.excess = {}
        if 'amount' not in item:
            item['amount'] = 1
        for r_name, r_amount in item['requires'].items():
            r_name = r_name.lower()
            if r_name in all_items:
                if r_name not in self.excess:
                    self.excess[r_name] = 0
                if self.excess[r_name] >= r_amount:
                    self.excess[r_name] -= r_amount
                else:
                    amount = 1
                    if 'amount' in all_items[r_name]:
                        amount = all_items[r_name]['amount']
                    for i in range(0, r_amount, amount):
                        self.get_requires(all_items[r_name], all_items, False)
                        self.excess[r_name] += amount  # dont add what you remove, potential bug if happens
            else:
                if r_name not in self.raw:
                    self.raw[r_name] = 0
                self.raw[r_name] += r_amount
        return self.raw


def load(file='items.skyfactory.json'):
    return {j.lower(): k for j, k in json.loads(''.join(open(file, 'r').readlines())).items()}


def main():
    items = load()
    make = input('What do you want to make? ').lower()
    amount = int(input('How many do you want to make? ') or '1')
    if make not in items:
        print('That item does not exist. Make sure you update the file with the recipe.')
        input('Press \'Enter\' when you are done updating the file.')
        load()
        if make in items:
            print('\nYou will require:')
            requires = Crafter().get_requires(items.get(make), items)
            for r in requires:
                print('  ' + str(requires[r] * amount) + ' of ' + r)
            another = input('\nWould you like to look up another (y or n)? ') == 'y'
            if not another:
                return False
        else:
            print('That item still does not exist!\n')
    else:
        requires = Crafter().get_requires(items.get(make), items)
        print('\nYou will require:')
        for r in requires:
            print('  ' + str(requires[r] * amount) + ' of ' + r)
        another = input('\nWould you like to look up another (y or n)? ') == 'y'
        if not another:
            return False


if __name__ == '__main__':
    while main():
        pass
