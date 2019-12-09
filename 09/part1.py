from intcode import cpu

test1 = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
test2 = '1102,34915192,34915192,7,4,7,99,0'
test3 = '104,1125899906842624,99'
input_code = open('09/code.int').readline().strip()

code = [int(i) for i in input_code.split(',')]

boost = cpu.Cpu(code)

while True:
    state = boost.run()
    if state[0] == 0:
        break
    elif state[0] == 1: 
        value = input('> ')
        boost.input(int(value))
    elif state[0] == 2:
        output = state[1]
        print(f'< {output}')