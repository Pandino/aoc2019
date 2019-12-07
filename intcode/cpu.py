class Cpu():
    '''Class representing a Intcode CPU.

    Initialize the class with the code to run (list of integers) and run() it.
    Assumption: destination parameters to write to are always last.
    Return codes: the main loop will return a tuple containing the exit code plus eventual parameters
    Exit codes:
        0 Program terminated without errors (i.e. reached instruction 99)
        1 Program paused waiting for input (use input(integer) and run() to continue it)
        2 Program sent an output value (as sole parameter). 
    '''

    def __init__(self, code, start=0, inputs=None, id=None):
        self.id = id
        self.code = code
        self.instruction_pointer = start
        self.cycle = 0
        if inputs is None:
            self.input_buffer = list()
        else:
            self.input_buffer = inputs

        # States
        self.done = False
        self.input_wait = False
        self.output_wait = False

    def _next(self, op_len):
        self.instruction_pointer += op_len

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

    def is_done(self):
        return self.done

    def input(self, value):
        self.input_buffer.append(value)

    def run(self):

        if self.done:
            raise Exception('Program already finished.')

        while True:
            opcode = self._get_opcode()
            skip = 1
            if opcode == 99:
                self.done = True
                return (0, )
            if opcode == 1:
                # ADD X, Y. Params: [In, In, Dest]. Len: 4
                result = sum(self._get_parameters(2))
                self._write(3, result)
                self._next(4)
            elif opcode == 2:
                # MUL X, Y. Params: [In, In, Dest]. Len: 4
                params = self._get_parameters(2)
                product = 1
                for param in params:
                    product *= param
                self._write(3, product)
                self._next(4)
            elif opcode == 3:
                # Save a number from Input. Params: [Out]. Len: 2
                if len(self.input_buffer) > 0:
                    self._write(1, self.input_buffer.pop())
                    self._next(2)
                else:
                    self.input_wait = True
                    return (1, )
            elif opcode == 4:
                # Send a number to Output. Params: [Out]. Len: 2
                output = self._get_parameters(1).pop()
                self._next(2)
                return (2, output)
            elif opcode == 5:
                # JNZ. Params: [In, In]. Len: 3
                test, dest = self._get_parameters(2)
                if test == 0:
                    self._next(3)
                else:
                    self.instruction_pointer = dest
            elif opcode == 6:
                # JZ. Params: [In, In]. Len: 3
                test, dest = self._get_parameters(2)
                if test == 0:
                    self.instruction_pointer = dest
                else:
                    self._next(3)
            elif opcode == 7:
                # Less than. Params: [In, In, Out]. Len: 4
                a, b = self._get_parameters(2)
                if a < b:
                    self._write(3, 1)
                else:
                    self._write(3, 0)
                self._next(4)
            elif opcode == 8:
                # EQ. Params: [In, In, Out]. Len: 4
                a, b = self._get_parameters(2)
                if a == b:
                    self._write(3, 1)
                else:
                    self._write(3, 0)
                self._next(4)
            else:
                raise Exception(f'Error. Unable to process op ({opcode}) at [{self.instruction_pointer}]')
            self.cycle += 1