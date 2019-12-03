from math import floor

total_fuel = 0

def fuel_requirement(mass):
    return floor(mass/3) - 2

def _fuel_iter(mass):
    fuel = fuel_requirement(mass)
    if fuel <= 0:
        return 0
    return fuel + _fuel_iter(fuel)
    

with open('a.input') as f:
    for line in f:
        total_fuel += _fuel_iter(int(line))
print(f'Total fuel required: {total_fuel}')