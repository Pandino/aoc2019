''' Input/output:
Input
a) Init class or cpu.run with list of input values
b) Break on input (exception, return code?) and wait for cpu.input(int) to continue 
c) Input buffer stack (FIFO) given as a), if empty b)

Output
a) break on output (this will break day 5 part 1) use cpu.get_output to retrieve the output value, use cpu.resume() to continue excecution
b) provide a function to run on output (?) 


Pseudocode
amplifiers = [ABCDEF]
ampli_cpus = [Cpu(code) for _ in ABCDEF]
for phases in possible_phase_vaues:
    input = 0
    for i, ampli in enumerate(ampli_cpus):
        ampli.run([input, phases[i]])
'''
from intcode import cpu
from itertools import permutations

test1 = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
test2 = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0' 
test3 = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'

with open('07/code.int') as f:
    code = [int(i) for i in f.readline().split(',')]

#code = [int(i) for i in test3.split(',')]

amplifiers = 'ABCDE'
best = (0,)
for phases in permutations([0,1,2,3,4]):
    cpus = [cpu.Cpu(code, id=name) for name in amplifiers]
    current_input = 0
    for phase, amp_cpu in zip(phases, cpus):
        amp_cpu.input(current_input)
        amp_cpu.input(phase)
        while True:
            state = amp_cpu.run()
            if state[0] == 0:
                break
            elif state[0] == 1:
                raise Exception(f'Input requred. phase: {phases}, cpu: {amp_cpu.id}')
            elif state[0] == 2:
                current_input = state[1]
    if current_input > best[0]:
        best = (current_input, phases)

print(f'Best output ({best[0]}) achieved using the phases: {"".join([str(p) for p in best[1]])}')