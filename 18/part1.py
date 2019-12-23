from collections import deque
from heapq import heappop, heappush
from itertools import combinations

class Maze():
    key_codes = 'abcdefghijklmnopqrstuvwxyz'
    door_codes = key_codes.upper()
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, filename):
        self.puzzle_map = dict()
        self.keys = dict()
        self.doors_to = dict()
        self.keys_to = dict()
        self.key_constrains = dict()
        self.cache = dict()
        self.max_x = 0
        self.max_y = 0
        self.start_points = list()
        with open(filename) as f:
            for y, line in enumerate(f):
                for x, point in enumerate(line.strip()):
                    self.puzzle_map[(x, y)] = point
                    if point == '@':
                        self.start_points.append((x, y))
                    if x > self.max_x: self.max_x = x
                    if y > self.max_y: self.max_y = y

    def _distance(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - b[0])

    def _is_key(self, current_pos, collected_keys):
        for key, pos in self.keys.items():
            if pos == current_pos and key not in collected_keys:
                return True
        return False

    def shortest_path(self, a, b):
        '''Find shortest path between a and b. Returns the steps needed.'''
        if (a, b) in self.cache:
            return self.cache[(a,b)]
        # print('c', end='', flush=True)    
        frontier = []
        come_from = {}
        cost_to = {}
        heappush(frontier, (0, a))
        come_from[a] = None
        cost_to[a] = 0

        while len(frontier) > 0:
            current = heappop(frontier)[1]

            if current == b:
                break

            for next_point in self._get_next_points(current):
                new_cost = cost_to[current] + 1
                if next_point not in cost_to or new_cost < cost_to[next_point]:
                    cost_to[next_point] = new_cost
                    priority = new_cost + self._distance(next_point, b)
                    heappush(frontier, (priority, next_point))
                    come_from[next_point] = current
        else:
            return None
        
        self.cache[(a, b)] = cost_to[b]
        return cost_to[b]

    def print_keys(self):
        for key, value in self.keys.items():
            x, y = value
            print(f'Key {key} at ({x}, {y}) blocked by [{self.doors_to[value]}], comes after [{self.keys_to[value][:-1]}]')

    def constrains(self):
        for key, key_pos in self.keys.items():
            constrains = frozenset(self.doors_to[key_pos].lower() + self.keys_to[key_pos][:-1])
            self.key_constrains[key] = constrains


    def find_keys(self):
        '''Breath first, find all keys and doors blocking them'''
        visited = set()
        pathes = deque()
        for start_point in self.start_points:
            pathes.append((start_point,))
            self.doors_to[start_point] = ''
            self.keys_to[start_point] = ''
            visited.add(start_point)
        while len(pathes) > 0:
            path = pathes.popleft()
            last_visited = path[-1]
            for point in self._get_next_points(last_visited):
                if point in visited:
                    continue
                symbol = self.puzzle_map[point]
                if symbol in self.door_codes:
                    self.doors_to[point] =  self.doors_to[last_visited] + symbol
                else:
                    self.doors_to[point] =  self.doors_to[last_visited]
                if symbol in self.key_codes:
                    self.keys[symbol] = point
                    self.keys_to[point] = self.keys_to[last_visited] + symbol
                else:
                    self.keys_to[point] = self.keys_to[last_visited]
                visited.add(point)
                new_path = path + (point, )
                pathes.append(new_path)

    def _get_next_points(self, point):
        x, y = point
        yield from ((x + d[0], y + d[1]) for d in self.directions if self.puzzle_map[(x + d[0], y + d[1])] != '#')

    def shortest_path_multi(self, start, b):
        result = list()
        for point in start:
            result.append(self.shortest_path(point, b))
        if len(result) > 1:
            return tuple(result)
        else:
            return result[0]
    
    def solve2(self):
        def reachable_steps(c_keys):
            for key, constrains in self.key_constrains.items():
                if key in c_keys:
                    continue
                current_constrains = constrains - set(c_keys)
                if len(current_constrains) == 0:
                    yield key

        steps_so_far = dict()
        graph = []
        start_points = tuple(self.start_points)
        heappush(graph, (0, start_points, ''))
        steps_so_far[(start_points, '')] = 0
        while graph:
            _, positions, keys = heappop(graph)
            
            if len(keys) == len(self.keys):
                return (steps_so_far[(positions, keys)])

            for next_key in reachable_steps(keys):
                next_pos = self.keys[next_key]
                new_collected_keys = keys + next_key
                key_index = ''.join(sorted(new_collected_keys))
                distances = self.shortest_path_multi(positions, next_pos)

                section = [i for i in range(len(distances)) if distances[i] is not None][0]
                new_steps = steps_so_far[(positions, keys)] + distances[section]
                new_positions = list(positions)
                new_positions[section] = next_pos
                new_positions = tuple(new_positions)

                if (new_positions, key_index) not in steps_so_far or steps_so_far[(new_positions, key_index)] > new_steps :
                        steps_so_far[(new_positions, key_index)] = new_steps
                        heappush(graph, (new_steps, new_positions, key_index))                

        return None



m = Maze('18/maze2')
m.find_keys()
m.print_keys()
m.constrains()
print(m.key_constrains)

print(m.solve2())