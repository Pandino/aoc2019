from math import floor

total_fuel = 0
with open('a.input') as f:
    for line in f:
        total_fuel += floor(int(line)/3) - 2
print(f'Total fuel required: {total_fuel}')