class Cpu():
    '''Class representing a Intcode CPU.

    Initialize the class with the code to run (list of integers) and run() it.
    Assumption: destination parameters to write to are always last.
    '''

    def __init__(self, code, start=0):
        self.code = code
        self.instruction_pointer = start
        self.cycle = 0

    def _get_instruction(self):
        '''Return the current instruction (modes+opcode)'''
        return self.code[self.instruction_pointer]

    def _get_opcode(self):
        '''Return the opcode of the current instruction'''
        instruction = self._get_instruction()
        return int(str(instruction)[-2:])

    def _get_modes(self, num_of_params):
        '''Return the num_of_params parameter modes of the current instruction'''
        instruction = self._get_instruction()
        template = '{:0>' + str(num_of_params + 2) + '}'
        normalized = template.format(str(instruction))[-3:(-4 - num_of_params):-1]
        return [int(mode) for mode in normalized]

    def _get_parameters(self, num_of_params):
        '''Get the required parameters of the current instruction'''
        modes = self._get_modes(num_of_params)
        params = list()
        for i, mode in enumerate(modes, start=1):
            ref = self.code[self.instruction_pointer + i]
            if mode == 0:
                params.append(self.code[ref])
            else:
                params.append(ref)
        return params[0:num_of_params]

    def _write(self, dest_param, data):
        '''Write data to the address specified in the nth dest_param'''
        dest = self.code[self.instruction_pointer + dest_param]
        self.code[dest] = data

    def run(self):

        while True:
            self.cycle += 1
            opcode = _get_opcode()
            skip = 1
            if opcode == 99:
                break        
            if opcode == 1:
                # Sum two numbers. Params: [In, In, Dest]. Len: 4
                result = sum(self._get_parameters(2))
                self._write(3, result)
                skip = 4
            elif opcode == 2:
                # Multiply two numbers. Params: [In, In, Dest]. Len: 4
                params = self._get_parameters(2)
                product = 1
                for param in params:
                    product *= param
                self._write(3, product)
                skip = 4
            elif opcode == 3:
                # Save a number from Input. Params: [Out]. Len: 2
                i = int(input('Input a number: '))
                self._write(1, i)
                skip = 2
            elif opcode == 4:
                # Send a number to Output. Params: [Out]. Len: 2
                output = self._get_parameters(1)
                print(output)
                skip = 2
            elif opcode == 5:
                test, dest = self._get_parameters(2)
                if test == 0:
                    skip = 3
                else:
                    skip = 0
                    self.instruction_pointer = dest
            elif opcode == 6:
                test, dest = self._get_parameters(2)
                if test == 0:
                    skip = 0
                    self.instruction_pointer = dest
                else:
                    skip = 3
            elif opcode == 7:
                a, b = self._get_parameters(2)
                if a < b:
                    self._write(3, 1)
                else:
                    self._write(3, 0)
                skip = 4
            elif opcode == 8:
                a, b = self._get_parameters(2)
                if a == b:
                    self._write(3, 1)
                else:
                    self._write(3, 0)
                skip = 4
            else:
                raise f'Error. Unable to process op ({opcode}) at [{self.instruction_pointer}]'
            self.instruction_pointer += skip