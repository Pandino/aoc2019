from collections import deque
from intcode.cpu import Cpu
import sys

class Switch():
    ''' Simulate a network of incode computers 
    '''
    
    def __init__(self, code, size):
        self.computers = [ Cpu(code, inputs=(i, ), id=i) for i in range(size) ]
        self.size = size
        self.nat = None

    def run(self):
        last_nat = None
        while True:
            print('.', end='')
            activity = False
            for computer in self.computers:
                state = computer.run()
                if state[0] == 0:
                    print(f'Computer {computer.id} terminated.')                    
                elif state[0] == 1:
                    computer.input(-1)
                elif state[0] == 2:
                    activity = True
                    dest = state[1]
                    sx, x = computer.run()
                    sy, y = computer.run()
                    if sx != 2 or sy != 2:
                        raise Exception(f'Bad return state {(sx, sy)}.')
                    if dest == 255:
                        self.nat = (x, y)                        
                        continue
                    self.computers[dest].input(x)
                    self.computers[dest].input(y)
            if not activity:
                if self.nat is not None:
                    x, y = self.nat
                    self.computers[0].input(x)
                    self.computers[0].input(y)
                    self.nat = None
                    print(y)
                    if y == last_nat:
                        print(f'NAT->[0] sent {y} twice in a row.')
                        sys.exit(0)
                    last_nat = y
                else:
                    print(f'All computers inactive.')

if __name__ == "__main__":
    with open('23/input.int') as f:
        code = [int(i) for i in f.readline().split(',')]
    switch = Switch(code, 50)
    switch.run()

