from intcode.cpu import Cpu
from collections import deque
from blessed import Terminal

class ASCII():

    movements = {1: (0, -1),  #North
                 2: (0, 1),   #South
                 3: (-1, 0),  #West
                 4: (1, 0) }  #East

    def __init__(self, code):
        self.code = code
        self.cpu = Cpu(code)
        self.term = Terminal()
        self.camera = dict()
        self.camera_x = 0
        self.camera_y = 0
        print(self.term.clear, end='')
        
    def run(self):
        while True:
            state = self.cpu.run()
            if state[0] == 0:
                break
            elif state[0] == 1:
                # Waiting for input
                pass
            elif state[0] == 2:
                self._update_camera(chr(state[1]))
                print(chr(state[1]), end='')

    def _update_camera(self, c):
        if c == '\n':
            self.camera_x = 0
            self.camera_y += 1
        else:
            self.camera[(self.camera_x, self.camera_y)] = c
            self.camera_x += 1

    def _reset_camera(self):
        self.camera_x = 0
        self.camera_y = 0
        self.camera = dict()

    def alignment(self):
        right = max([x for x, _ in self.camera])
        bottom = max([y for _, y in self.camera])
        total = 0
        for y in range(2, bottom-2):
            for x in range(2, right-2):
                if self.camera[(x, y)] == '#':
                    cross = [(x + direction[0], y + direction[1]) for direction in self.movements.values()]
                    if all([self.camera[neighbor] == '#' for neighbor in cross]):
                        total += x*y
        return total

with open('17/puzzle_input.int') as f:
    code = [int(i) for i in f.readline().split(',')]

camera = ASCII(code)
camera.run()
print(camera.alignment())
