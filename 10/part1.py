from math import gcd

maps = list()
with open('10/tests') as f:
    asteroid_map = ''
    for line in f:
        if line.strip() == '':
            maps.append(asteroid_map)
            asteroid_map = ''
        else:
            asteroid_map += line

class Asteroids():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def angle_from(self, other):
        if self == other:
            return 0
        x = self.x + other.x
        y = self.y + other.y
        common_denominator = gdc(x, y)
        return (x/common_denominator, y/common_denominator)

    def __eq__(self, other):
        
        return self.x == other.x and self.y == other.y

    

asteroid_map = maps[0]

asteroids = list()

for y, line in enumerate(asteroid_map.splitlines()):
    for x, point in enumerate(line):
        if point == '#':
            asteroids.append(Asteroids(x, y))

print(asteroids)