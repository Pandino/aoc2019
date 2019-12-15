import re
from math import ceil

'''
Given desidered product (FUEL) and quantity (1):
 starting witht the desidered product:
     add the produced amount in inventory
     add the required amount to required_ragents
 for each required_reagent:
     if reagent not in inventory:
        add produced amount to inventory (production + inventory should be > than required)
        add required amount to required_reagents
     else subtract from inventory
 until
     all required reagents don't have an associated reaction (ORE)

 
'''

chemical_match = re.compile(r'(\d+) ([A-Z]+)')

test1 = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

test2 = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

test3 = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''

test4 = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''

test5 = '''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX'''


class Reaction():
    def __init__(self, product, quantity):
        self.reagents = dict()
        self.product = product
        self.quantity = quantity

    def add_reagent(self, name, amount):
        self.reagents[name] = amount

    def chemical_names(self):
        ''' Return all chemicals involved in the reaction'''
        result = [name for name in self.reagents.keys()]
        result.append(self.product)
        return tuple(result)
        

    def __str__(self):
        reagents = ', '.join([f'{n} {name}' for name, n in self.reagents.items()])
        product = f'{self.quantity} {self.product}'
        return f'{reagents} => {product}'

class NanoFactory():
    def __init__(self, puzzle_input):
        self.reactions = dict()
        self.inventory = dict()
        self.required_amounts = dict()
        self._parser(puzzle_input)
        self._init_dicts()

    def _init_dicts(self):
        for reaction in self.reactions.values():
            for chemical in reaction.chemical_names():
                self.inventory[chemical] = 0
                self.required_amounts[chemical] = 0

    def resolveb(self):
        finished = False
        while not finished:
            print(self.required_amounts)
            print(self.inventory)
            print('---------')
            finished = True
            for chemical in list(self.required_amounts.keys()):
                if chemical not in self.reactions:
                    continue
                
                finished = False
                                
                required_amount = self.required_amounts[chemical]
                if required_amount <= self.inventory[chemical]:
                    # We have enough in the inventory
                    self.inventory[chemical] -= required_amount
                    del self.required_amounts[chemical] 
                else:
                    # Produce it
                    reaction = self.reactions[chemical]
                    amount_to_produce = required_amount - self.inventory[chemical]
                    multiplier = 1
                    if amount_to_produce > reaction.quantity:
                        multiplier = ceil(amount_to_produce/reaction.quantity)
                    self.inventory[chemical] += reaction.quantity * multiplier - required_amount
                    del self.required_amounts[chemical]
                    for reagent, reagent_amount in reaction.reagents.items():
                        if reagent in self.required_amounts:
                            self.required_amounts[reagent] += reagent_amount * multiplier
                        else:
                            self.required_amounts[reagent] = reagent_amount * multiplier



    def _parser(self, lines):
        for line in lines:
            reaction = None
            left_chems, right_chem = line.split('=>')
            match = chemical_match.match(right_chem.strip())
            if match:
                reaction = Reaction(match.group(2), int(match.group(1)))
            else:
                raise Exception('Unable to parse: ' + line)
            for chemical in left_chems.split(','):
                match = chemical_match.match(chemical.strip())
                if match:
                    reaction.add_reagent(match.group(2), int(match.group(1)))
                else:
                    raise Exception('Unable to parse: ' + line)
            if reaction is not None:
                self.reactions[reaction.product] = reaction
            else:
                raise Exception('Failed to parse: ' + line)

with open('14/puzzle_input') as f:
    puzzle_input = f.readlines()

factory = NanoFactory(puzzle_input)
print([str(reaction) for reaction in factory.reactions.values()])
factory.required_amounts['FUEL'] = 1
factory.resolveb()