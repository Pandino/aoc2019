import sys

test = '''....#
#..#.
#..##
..#..
#....'''

puzzle_input = '''####.
.##..
##.#.
###..
##..#''' 

class Layout():
    def __init__(self, ascii_map):
        self.map = [[True if point == '#' else False for point in line.strip()] for line in ascii_map.split('\n')]

    def print(self):
        for y in range(5):
            for x in range(5):
                print('#' if self.map[y][x] else '.', end= '')
            print()
    
    def update(self):
        changes = list()
        adiacent_coords = ((0, 1), (0, -1), (1, 0), (-1, 0))
        for y in range(5):
            for x in range(5):
                neigthbors = sum(1 for (dx, dy) in adiacent_coords if self._find_safe(x+dx, y+dy))
                if self.map[y][x]:
                    if neigthbors != 1:
                        changes.append((x, y))
                else:
                    if neigthbors == 1 or neigthbors == 2:
                        changes.append((x, y))
        
        if len(changes) == 0:
            print('Simulation reached a stable state')
            raise Exception('Reached final state')

        for x, y in changes:
            self.map[y][x] = not self.map[y][x]
        

    def _find_safe(self, x, y):
        '''Retrieve value at (x, y) in the map. If (x, y) is outbund return False'''
        if x < 0 or x >= 5 or y < 0 or y >= 5:
            return False
        return self.map[y][x]

    def hash(self):
        return sum(2**pos for pos, v in enumerate(self._iterate_map()) if v is True)
            

    def _iterate_map(self):
        for y in range(5):
            for x in range(5):
                yield self.map[y][x]

if __name__ == "__main__":
    history = set()
    layout = Layout(puzzle_input)
    history.add(layout.hash())
    while True:
        layout.update()
        hashed = layout.hash()
        if hashed in history:
            print(f'Found duplicate layout with hash: {hashed}')
            sys.exit(0)
        history.add(hashed)
