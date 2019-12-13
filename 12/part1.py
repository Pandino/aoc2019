import re
from itertools import combinations

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
    def apply_velocity(self):
        self.position = [position + velocity for position, velocity in zip(self.position, self.velocity)]

    def total_energy(self):
        return sum([abs(i) for i in self.position]) * sum([abs(i) for i in self.velocity])

    def __repr__(self):
        return f'pos={self._print_vector(self.position)}, vel={self._print_vector(self.velocity)})'
    def _print_vector(self, v):
        return('<x={:2}, y={:2}, z={:2}>'.format(v[0], v[1], v[2]))

class Simulation():
    def __init__(self, moons):
        self.moons = moons
        self.steps = 0

    def run(self, steps):
        while self.steps < steps:
            self._apply_gravity()
            self._apply_velocity()
            self.steps += 1

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
    simulation.run(1000)
    for moon in simulation.moons:
        print(moon)
    print(simulation.total_energy())