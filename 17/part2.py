from intcode.cpu import Cpu
from collections import deque
from blessed import Terminal

class Drone():

 
    def __init__(self, code, solutions):
        self.code = code
        self.cpu = Cpu(code)
        self.solutions = solutions
 
        
    def run(self):
        while True:
            state = self.cpu.run()
            if state[0] == 0:
                break
            elif state[0] == 1:
                # Waiting for input
                self.send(self.solutions.pop(0))
            elif state[0] == 2:
                if state[1] > 100:
                    print(state[1])
                else:
                    print(chr(state[1]), end='')
    
    def send(self, data):
        for c in data:
            self.cpu.input(ord(c))

    

with open('17/puzzle_input.int') as f:
    code = [int(i) for i in f.readline().split(',')]

solution = [
    'A,C,A,B,C,A,B,A,B,C\n',
    'L,12,L,8,L,8\n'
    'R,4,L,12,L,12,R,6\n',
    'L,12,R,4,L,12,R,6\n',
    'n\n'
]
code[0] = 2
drone = Drone(code, solution)
drone.run()

