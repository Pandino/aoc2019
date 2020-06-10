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
    def __init__(self, ascii_map=None, level=0):
        if ascii_map is None:
            self.map = [[False for _ in range(5)] for _ in range(5)]
        else:
            self.map = [[True if point == '#' else False for point in line.strip()] for line in ascii_map.split('\n')]
        self.changes = list()
        self.level = level
        self._hash = None

    def print(self):
        print(f'Depth {self.level}:')
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 2:
                    print('?', end='')
                else:
                    print('#' if self.map[y][x] else '.', end= '')
            print()
    
    def calculate(self, inner, outer):        
        
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 2:
                    continue
                neigthbors = sum(1 for bug in self._find_safe(x, y, inner, outer) if bug is True)
                if self.map[y][x]:
                    if neigthbors != 1:
                        self.changes.append((x, y))
                else:
                    if neigthbors == 1 or neigthbors == 2:
                        self.changes.append((x, y))
        
    def update(self):
        if len(self.changes) > 0:
            for x, y in self.changes:
                self.map[y][x] = not self.map[y][x]
            self.changes = list()
            self._hash = None
        

    def _find_safe(self, ox, oy, inner, outer):
        '''Retrieve value at (x, y) in the map.'''
        cardinal_points = ((0, 1), (1, 0), (0, -1), (-1, 0))
        if inner:
            inner_bugs = inner.get_outer_border()
        else:
            inner_bugs = [[False for _ in range(5)] for _ in range(4)]
        if outer:
            outer_bugs = outer.get_inner_border()
        else:
            outer_bugs = [False, False, False, False]
        for x, y, dx, dy in ((ox+dx, oy+dy, dx, dy) for dx, dy in cardinal_points):
            if y == -1: #N
                yield outer_bugs[0]
            elif x == 5: #E
                yield outer_bugs[1]
            elif y == 5: #S
                yield outer_bugs[2]
            elif x == -1: #W
                yield outer_bugs[3]
            elif (x, y) == (2, 2):
                if dy == 1: #N
                    yield from inner_bugs[0]
                if dx == -1: #E
                    yield from inner_bugs[1]
                if dy == -1: #S
                    yield from inner_bugs[2]
                if dx == 1: #W
                    yield from inner_bugs[3]
            else:
                yield self.map[y][x]
        
        
        
    def get_inner_border(self):
        '''Returns inner border clockwise from N'''
        inner_coords = ((1,2),(2,3),(3,2),(2,1))
        return [self.map[y][x] for y, x in inner_coords]

    def get_outer_border(self):
        outer_coords = (
            ((x, 0) for x in range(5)),
            ((4, y) for y in range(5)),
            ((x, 4) for x in range(5)),
            ((0, y) for y in range(5)),
        )
        return [[self.map[y][x] for x, y in border] for border in outer_coords]

    def hash(self):
        if not self._hash:
            self._hash = sum(2**pos for pos, v in enumerate(self._iterate_map()) if v is True)
        return self._hash

    def count(self):
        return sum(1 for pos in self._iterate_map() if pos is True)
            

    def _iterate_map(self):
        for y in range(5):
            for x in range(5):
                yield self.map[y][x]

class Simulator():
    def __init__(self, level_zero):
        self.layouts = dict()
        self.layouts[0] = Layout(level_zero)
        self.layouts[1] = self.innest = Layout(level=1)
        self.layouts[-1] = self.outest = Layout(level=-1)
        
    def step(self):

        if self.innest.hash() > 0:
            level = self.innest.level
            self.layouts[level+1] = self.innest = Layout(level=level+1)
        if self.outest.hash() > 0:
            level = self.outest.level
            self.layouts[level-1] = self.outest = Layout(level=level-1)
        for level, layout in self.layouts.items():
            if layout == self.innest:
                layout.calculate(None, self.layouts[level-1])
            elif layout == self.outest:
                layout.calculate(self.layouts[level+1], None)
            else:
                layout.calculate(self.layouts[level+1], self.layouts[level-1])
        for level, layout in self.layouts.items():
            layout.update()

    def print(self):
        for level in sorted(self.layouts):
            self.layouts[level].print()
            print()

    def count(self):
        return sum(layout.count() for layout in self.layouts.values())

if __name__ == "__main__":
    sim = Simulator(puzzle_input)
    
    for _ in range(200):
        sim.step()
    
    
    print(sim.count())
    
