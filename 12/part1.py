import re
from itertools import combinations
from math import gcd

aoc_input='''<x=16, y=-8, z=13>
<x=4, y=10, z=10>
<x=17, y=-5, z=6>
<x=13, y=-3, z=0>'''

### TEST CASES ###
# aoc_input='''<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>'''
# aoc_input='''<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>'''

class Moon():
    def __init__(self, position, velocity=None):
        self.position = position
        self.velocity = [0, 0, 0]
        self.orbital_period = None

    def apply_velocity(self):
        self.position = [position + velocity for position, velocity in zip(self.position, self.velocity)]

    def total_energy(self):
        return sum([abs(i) for i in self.position]) * sum([abs(i) for i in self.velocity])

    def __hash__(self):
        return hash((tuple(self.position), tuple(self.velocity)))

    def __eq__(self, other):
        return tuple(self.position) == tuple(other.position) and tuple(self.velocity) == tuple(other.velocity)

    def __repr__(self):
        return f'pos={self._print_vector(self.position)}, vel={self._print_vector(self.velocity)})'
    def _print_vector(self, v):
        return('<x={:2}, y={:2}, z={:2}>'.format(v[0], v[1], v[2]))

class Simulation():
    def __init__(self, moons):
        self.moons = moons
        self.steps = 0

    def run(self, steps):
        original_state = [hash(moon) for moon in self.moons]
        while self.steps < steps:
            if all([moon.orbital_period is not None for moon in self.moons]):
                break
            self._apply_gravity()
            self._apply_velocity()
            self.steps += 1
            for n, moon in enumerate(self.moons):
                if hash(moon) == original_state[n]:
                    if moon.orbital_period is None:
                        print(f'Moon {n} original state at {self.steps}')
                        moon.orbital_period = self.steps
        else:
            print('Couldn\'t find all original states')

    def total_energy(self):
        return sum([moon.total_energy() for moon in self.moons])

    def _apply_gravity(self):
        for a, b in combinations(self.moons, 2):
            for axis in range(3):
                if a.position[axis] > b.position[axis]:
                    a.velocity[axis] -= 1
                    b.velocity[axis] += 1
                elif a.position[axis] < b.position[axis]:
                    a.velocity[axis] += 1
                    b.velocity[axis] -= 1

    def _apply_velocity(self):
        for moon in self.moons:
            moon.apply_velocity()

def lcm(values):
    def _lcm(a, b):
        return a * b // gcd(a, b)
    result = 1
    for value in values:
        result = _lcm(result, value)
    return result


if __name__ == '__main__':
    moons = list()
    for line in aoc_input.splitlines():
        match = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line.strip())
        if match:
            position  = [ int(i) for i in match.group(1, 2, 3) ]
            moons.append(Moon(position))
        else:
            raise Exception('Error parsing: ' + line)

    simulation = Simulation(moons)
    simulation.run(100000000000)
    if any([moon.orbital_period is None for moon in moons]):
        print('Skip')
    else:
        part2 = lcm([moon.orbital_period for moon in moons])
        print(f'Steps to initial state: {part2}')
    # for moon in moons:
        # print(moon.orbital_period)
    # print(simulation.total_energy())