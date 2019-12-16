from intcode.cpu import Cpu

class RepairDrone():
    def __init__(self, code):
        self.cpu = cpu.Cpu(code)
        
    def run(self):
        while True:
            state = self.cpu.run()
            if state[0] == 0:
                break
            elif state[0] == 1:
                # Waiting for input
                pass
            elif state[0] == 2:
                # Waiting to process output
                pass

    def scan_area(self):
        ''' pseudocode:
        - Add current position (0, 0) to map.
        - 


with open('15/puzzle_input.int') as f:
    code = [int(i) for i in f.readline().split(',')

robot = RepairDrone(code)
map = robot.scan_area()