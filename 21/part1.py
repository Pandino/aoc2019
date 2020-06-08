# jump is 4 steps
# D must always be true
# any of the others must be False

from intcode.ascii import Ascii

with open('21/puzzle_input.int') as f:
    code = [int(i) for i in f.readline().split(',')]

with open('21/jumper_run.ss') as f:
    test = f.read() + '\n'
drone = Ascii(code, test)
drone.run()
