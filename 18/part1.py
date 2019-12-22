from collections import deque
from heapq import heappop, heappush

class Key():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.constrains = set()

class Dependencies():
    def __init__(self):
        self.keys = set()
    
    def add_constrain(self, key, constrain):
        pass

class Maze():
    key_codes = 'abcdefghijklmnopqrstuwxyz'
    door_codes = key_codes.upper()
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, filename):
        self.puzzle_map = dict()
        self.keys = dict()
        self.doors_to = dict()
        self.keys_to = dict()
        self.key_constrains = dict()
        with open(filename) as f:
            for y, line in enumerate(f):
                for x, point in enumerate(line.strip()):
                    self.puzzle_map[(x, y)] = point
                    if point == '@':
                        self.start_point = (x, y)
                    # elif point in Maze.key_codes:
                    #     self.keys[point] = (x, y)
                    # elif point in Maze.door_codes:
                    #     self.doors[point] = (x, y)

    def _distance(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - b[0])

    def _is_key(self, current_pos, collected_keys):
        for key, pos in self.keys.items():
            if pos == current_pos and key not in collected_keys:
                return True
        return False

    def shortest_path(self, a, b, collected_keys):
        '''Find shortest path between a and b. Returns the steps needed.'''
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
                if self._is_key(next_point, collected_keys):
                    continue
                if next_point not in cost_to or new_cost < cost_to[next_point]:
                    cost_to[next_point] = new_cost
                    priority = new_cost + self._distance(next_point, b)
                    heappush(frontier, (priority, next_point))
                    come_from[next_point] = current
        else:
            return None
        
        return cost_to[b]

    def print_keys(self):
        for key, value in self.keys.items():
            x, y = value
            print(f'Key {key} at ({x}, {y}) blocked by [{self.doors_to[value]}], comes after [{self.keys_to[value][:-1]}]')

    def constrains(self):
        for key, key_pos in self.keys.items():
            constrains = self.doors_to[key_pos].lower() + self.keys_to[key_pos][:-1]
            self.key_constrains[key] = constrains


    def find_keys(self):
        '''Breath first, find all keys and doors blocking them'''
        visited = set()
        x, y = self.start_point
        pathes = deque( [(self.start_point,)] )
        self.doors_to[self.start_point] = ''
        self.keys_to[self.start_point] = ''
        visited.add(self.start_point)
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
        return [(x + d[0], y + d[1]) for d in self.directions if self.puzzle_map[(x + d[0], y + d[1])] != '#']

    def solve(self):
        def reachable_steps(collected_keys):
            result = list()
            for key, p in self.keys.items():
                if key in collected_keys:
                    continue
                doors = set(self.doors_to[p]) - set([s.upper() for s in collected_keys])
                if len(doors) == 0:
                    result.append(key)
            return result                

        graph = []
        heappush(graph, (0, 0, self.start_point, ''))
        while len(graph) > 0:
            _, steps, current_pos, collected_keys = heappop(graph)
            if len(collected_keys) == len(self.keys):
                return (steps, collected_keys)
            
            # print(steps, collected_keys)
                    

            for next_key in reachable_steps(collected_keys):
                next_pos = self.keys[next_key]
                new_collected_keys = collected_keys + next_key
                distance = self.shortest_path(current_pos, next_pos, new_collected_keys)
                if distance is None:
                    continue
                new_steps = steps + distance
                priority = new_steps
                heappush(graph, (priority, new_steps, next_pos, new_collected_keys))
                

        return None





m = Maze('18/test1')
m.find_keys()
m.print_keys()
m.constrains()
print(m.key_constrains)
print(m.solve())