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

class Vector1():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.orbital_period = None

    def __eq__(self, other):
        if isinstance(other, Vector1):
            return self.position == other.position and self.velocity == other.velocity
        return NotImplemented

    def __hash__(self):
        return hash((self.position, self.velocity))

class Simulation():
    def __init__(self, positions):
        self.vectors = [Vector1(p, v) for p, v in zip(positions, [0] * len(positions))]
        self.origin_vectors = [Vector1(p, v) for p, v in zip(positions, [0] * len(positions))]
        self.steps = 0

    def run(self, step_limit):
        '''
        run model:
        for each moon
        for each axis
        if original state => save steps period
        once all vectors have a period:
        calculate lcm
        '''
        while self.steps < step_limit:
            self._apply_gravity()
            self._apply_velocity()
            self.steps += 1
            # for vector, origin in zip(self.vectors, self.origin_vectors):
            #     if vector == origin and vector.orbital_period is None:
            #         vector.orbital_period = self.steps
            if all([vector == original for vector, original in zip(self.vectors, self.origin_vectors)]):
                return self.steps
        return None
        

    def _apply_gravity(self):
        for a, b in combinations(self.vectors, 2):
            if a.position > b.position:
                a.velocity -= 1
                b.velocity += 1
            elif a.position < b.position:
                a.velocity += 1
                b.velocity -= 1

    def _apply_velocity(self):
        for vector in self.vectors:
            vector.position += vector.velocity

    def get_period(self):
        if any([vector.orbital_period is None for vector in self.vectors]):
            return None
        else:
            return lcm([vector.orbital_period for vector in self.vectors])

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
            moons.append(position)
        else:
            raise Exception('Error parsing: ' + line)

    x, y, z = zip(*moons)
    simulation = Simulation(x)
    rx = simulation.run(100000000000)
    simulation = Simulation(y)
    ry = simulation.run(100000000000)
    simulation = Simulation(z)
    rz = simulation.run(100000000000)
    print(rx, ry, rz)
    print(lcm((rx, ry, rz)))