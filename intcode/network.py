#Implementation of a networked Intcode computer

from intcode.cpu import Cpu
from blessed import Terminal
from collections import deque

class Netcode():
    def __init__(self, code, id):
        self.code = code
        self.cpu = Cpu(code, id=id, inputs=(id, ))
        self.network_buffer = deque()

    def run(self):
        while True:
            state = self.cpu.run()
            if state[0] == 0:
                print('Intcode Execution Terminated')
                break
            elif state[0] == 1:
                # Waiting for input
                if self.batch:
                    self.send(self.batch)
                else:
                    self.send(input() + '\n')
            elif state[0] == 2:
                if state[1] > 256:
                    print(state[1])
                else:
                    print(chr(state[1]), end='')
    
    def send(self, data):
        for c in data:
            self.cpu.input(ord(c))