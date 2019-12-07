from intcode import cpu
from itertools import permutations

test1 = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
test2 = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0' 
test3 = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'


test4 = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
test5 = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

with open('07/code.int') as f:
    code = [int(i) for i in f.readline().split(',')]

#code = [int(i) for i in test5.split(',')]

amplifiers = 'ABCDE'
best = (0,)
for phases in permutations([5,6,7,8,9]):
    cpus = [cpu.Cpu(code[:], id=name) for name in amplifiers]
    current_input = 0
    finished = False
    
    # setup the cpus
    for phase, amp_cpu in zip(phases, cpus):
        amp_cpu.input(phase)
        while True:
            state = amp_cpu.run()
            if state[0] == 1:
                break
            else:
                raise Exception(f'Unexpected return state during initialization.')
    
    while not finished:
        for amp_cpu in cpus:
            amp_cpu.input(current_input)
            while True:
                state = amp_cpu.run()
                if state[0] == 0:
                    #print(f'Cpu {amp_cpu.id} terminated')
                    finished = True
                    break
                elif state[0] == 1: 
                    #print(f'Cpu {amp_cpu.id} waiting for input. i={amp_cpu.code[28]}')
                    break
                elif state[0] == 2:
                    current_input = state[1]
                    #print(f'Cpu {amp_cpu.id} output: {current_input}')
    if current_input > best[0]:
        best = (current_input, phases)

print(f'Best output ({best[0]}) achieved using the phases: {"".join([str(p) for p in best[1]])}')