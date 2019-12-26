from intcode.cpu import Cpu
from blessed import Terminal
from heapq import heappop, heappush

class TargetDrone():
    
    def __init__(self, code):
        self.code = code
        self.cpu = Cpu(code)
        self.term = Terminal()

    def deploy(self, coords):
        self.cpu.reset()
        self.cpu.input(coords[0])
        self.cpu.input(coords[1])
        result = self.cpu.run()
        if result[0] == 2:
            return result[1]
        
def search(drone):
    '''Starting from (100,0) go down until a # is found. Then check if the square would fit, if not go first right and then down, following the ray'''
    def test(x, y):
        if drone.deploy((x - 99, y + 99)) == 1:
            return True
        return False
    
    x = 100
    y = 0
    while True:
        if test(x, y):
            return x - 99, y
        if drone.deploy((x+1, y)):
            x += 1
            continue
        y = y + 1     

with open('19/code.int') as f:
    code = [int(i) for i in f.readline().split(',')]

target = TargetDrone(code)

# total = 0
# for y in range(0, 50):
#     for x in range(0, 50):
#         total += target.deploy((x, y))       
# print(total)

x, y = search(target)

print(x*10000+y)