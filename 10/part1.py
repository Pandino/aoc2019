from math import gcd, atan2, pi

maps = list()
with open('10/tests') as f:
    asteroid_map = ''
    for line in f:
        if line.strip() == '':
            maps.append(asteroid_map)
            asteroid_map = ''
        else:
            asteroid_map += line

def convert_angle(angle):
    '''Convert geometrical coordinates to radiants. Zero degrees is along the positive y axis and increase clockwise'''
    r = atan2(*angle)
    if r < 0:
        r = (pi + r) + pi
    return r

class Asteroids():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def angle_from(self, other):
        if self == other:
            return 0
        x = self.x - other.x
        y = self.y - other.y
        common_denominator = gcd(x, y)
        return (x//common_denominator, y//common_denominator)

    def rel_distance(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return (x^2 + y^2)

    def __eq__(self, other):
        if isinstance(other, Asteroids):
            return self.x == other.x and self.y == other.y
        raise NotImplementedError()

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'Asteroids({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    

asteroid_map = maps[0]

asteroids = list()

for y, line in enumerate(asteroid_map.splitlines()):
    for x, point in enumerate(line.strip()):
        if point == '#':
            asteroids.append(Asteroids(x, y))

highest_targets = 0
monitoring_station = None
for asteroid in asteroids:
    visited = set()
    for target in asteroids:
        if asteroid == target:
            continue
        angle = asteroid.angle_from(target)
        visited.add(angle)
    if len(visited) > highest_targets:
        highest_targets = len(visited)
        monitoring_station = asteroid

print(f'Best asteriod is {monitoring_station} with a view of {highest_targets} asteroids.')

asteroids_by_angle = dict()

for asteroid in asteroids:
    angle = monitoring_station.angle_from(asteroid)
    if angle not in asteroids_by_angle:
        asteroids_by_angle[angle] = list()
    asteroids_by_angle[angle].append(asteroid)

for angle in asteroids_by_angle.keys():
    asteroids_by_angle[angle] = sorted(asteroids_by_angle[angle], key=lambda target: monitoring_station.rel_distance(target))

for angle in asteroids_by_angle.keys():
    print(asteroids_by_angle[angle])
