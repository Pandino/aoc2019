from intcode.cpu import Cpu
from collections import deque
import random
from blessed import Terminal

class RepairDrone():

    movements = {1: (0, -1),  #North
                 2: (0, 1),   #South
                 3: (-1, 0),  #West
                 4: (1, 0) }  #East

    def __init__(self, code):
        self.code = code
        self.cpu = Cpu(code)
        self.term = Terminal()
        print(self.term.clear, end='')
        
    def run(self, path):
        for move in path:
            self.cpu.input(move)

        while True:
            state = self.cpu.run()
            if state[0] == 0:
                break
            elif state[0] == 1:
                # Waiting for input
                pass
            elif state[0] == 2:
                if len(self.cpu.input_buffer) == 0:
                    return state[1]
                if state[1] == 2:
                    print('WTFFFFFF?????')

    def scan_area(self):
        ''' pseudocode:
        - Add current position (0, 0) to map.
        - Prepare empty path queue: (dest_coords, (path to explore using drone commands))
        - Add first four paths
        - for each path in queue (FIFO), until queue is empty:
          - simulate it (keeping track of coords)
          - save result of last step in the map 
          - if result is not a wall: add resulting path to queue
        '''
        directions = [1, 2, 3, 4]
        puzzle_map = {(0, 0): 1}
        path_queue = deque([((0 + x, 0 + y), (direction, )) for direction, (x, y) in self.movements.items()])
        while len(path_queue) > 0:
            dest_coords, path = path_queue.popleft()
            self.cpu.reset()
            output = self.run(path)
            if dest_coords in puzzle_map and puzzle_map[dest_coords] is not None and puzzle_map[dest_coords] != output:
                print('Something wrong here!' + str(dest_coords) + len(path))
                break
            puzzle_map[dest_coords] = output
            if output == 2:
                self.print_map(puzzle_map)
                print(f'DEST FOUND AT {dest_coords} after {len(path)} steps')
                break
            if output != 0:
                #random.shuffle(directions)
                for direction in directions:
                    (x, y) = self.movements[direction]
                    new_coords = (dest_coords[0] + x, dest_coords[1] + y)
                    if new_coords not in puzzle_map:
                        puzzle_map[new_coords] = None
                        path_queue.append((new_coords, path + (direction, )))
        print()
        return puzzle_map

    def print_map(self, puzzle_map):
        print(self.term.clear, end='')
        min_x = min([x for x, _ in puzzle_map])
        min_y = min([y for _, y in puzzle_map])
        max_x = max([x for x, _ in puzzle_map])
        max_y = max([y for _, y in puzzle_map])

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if x == 0 and y == 0:
                    tile = '&'
                elif (x, y) not in puzzle_map:
                    tile = ' '
                else:
                    tile = puzzle_map[(x, y)]
                    if tile is None:
                        tile = '?'
                    else:
                        tile = ('#', '.', '@')[tile]
                print(self.term.move(y - min_y, x - min_x) + tile, end='')
        print(flush=True)
        




with open('15/puzzle_input.int') as f:
    code = [int(i) for i in f.readline().split(',')]

robot = RepairDrone(code)
robot.scan_area()
