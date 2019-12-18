from collections import deque

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

    def __init__(self, code, inputs=None, id=None):
        self.id = id
        self.rom = { key: value for (key, value) in enumerate(code)}
        
        self.reset()
        if inputs is not None:
            self.input_buffer = deque(inputs)
        
        
    def reset(self):        
        self.code = self.rom.copy()
        self.relative_base = 0
        self.cycle = 0
        self.done = False
        self.input_wait = False
        self.output_wait = False
        self.input_buffer = deque()
        self.instruction_pointer = 0
    
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
        '''Return a list of parameters of the current instruction.
        Parameters are represented as tuples of the mode and the value as it appears in the instruction.
        num_of_params is the number of parameters expected by the opcode.
        '''
        modes = self._get_modes(num_of_params)
        params = list()
        for i, mode in enumerate(modes, start=1):
            ref = self._read(self.instruction_pointer + i)
            params.append((mode, ref))
        return params

    def _resolve_parameter(self, parameter):
        '''given the provided parameter (as a tuple of mode and intruction parameter), retrieve its value from memory'''
        
        mode, ref = parameter        
        # Position mode
        if mode == 0:
            return self._read(ref)
        # Immediate mode
        elif mode == 1:
            return ref
        # Relative mode
        elif mode == 2:
            return self._read(self.relative_base + ref)
        else:
            raise Exception(f'Unsupported mode {mode} at address {self.instruction_pointer}')

    def _write_parameter(self, dest_param, data):
        '''Write data to the address specified in the nth dest_param'''
        mode, ref = dest_param
        if mode == 0:
            self.code[ref] = data
        elif mode == 1:
            raise Exception(f'Illegal immediate mode for a writing action. Address: {self.instruction_pointer}')
        elif mode == 2:
            self.code[self.relative_base + ref] = data

    def _read(self, address):
        '''Read an address in memory'''
        if address in self.code:
            return self.code[address]
        return 0

    def is_done(self):
        return self.done

    def input(self, value):
        self.input_buffer.append(value)

    def run(self):

        if self.done:
            raise Exception('Program already finished.')
        self.output_wait = False

        while True:
            opcode = self._get_opcode()
            if opcode == 99:
                self.done = True
                return (0, )
            if opcode == 1:
                # ADD X, Y. Params: [In, In, Dest]. Len: 4
                params = self._get_parameters(3)
                result = sum(self._resolve_parameter(param) for param in params[0:2])
                self._write_parameter(params[2], result)
                self._next(4)
            elif opcode == 2:
                # MUL X, Y. Params: [In, In, Dest]. Len: 4
                params = self._get_parameters(3)
                product = 1
                for param in params[0:2]:
                    product *= self._resolve_parameter(param)
                self._write_parameter(params[2], product)
                self._next(4)
            elif opcode == 3:
                # Save a number from Input. Params: [Out]. Len: 2
                if len(self.input_buffer) > 0:
                    params = self._get_parameters(1)
                    self._write_parameter(params[0], self.input_buffer.popleft())
                    self.input_wait = False
                    self._next(2)
                else:
                    self.input_wait = True
                    return (1, )
            elif opcode == 4:
                # Send a number to Output. Params: [Out]. Len: 2
                params = self._get_parameters(1)
                output = self._resolve_parameter(params[0])
                self.output_wait = True
                self._next(2)
                return (2, output)
            elif opcode == 5:
                # JNZ. Params: [In, In]. Len: 3
                params = self._get_parameters(2)
                test = self._resolve_parameter(params[0])
                dest = self._resolve_parameter(params[1])
                if test == 0:
                    self._next(3)
                else:
                    self.instruction_pointer = dest
            elif opcode == 6:
                # JZ. Params: [In, In]. Len: 3
                params = self._get_parameters(2)
                test = self._resolve_parameter(params[0])
                dest = self._resolve_parameter(params[1])
                if test == 0:
                    self.instruction_pointer = dest
                else:
                    self._next(3)
            elif opcode == 7:
                # Less than. Params: [In, In, Out]. Len: 4
                params = self._get_parameters(3)
                a = self._resolve_parameter(params[0])
                b = self._resolve_parameter(params[1])
                if a < b:
                    self._write_parameter(params[2], 1)
                else:
                    self._write_parameter(params[2], 0)
                self._next(4)
            elif opcode == 8:
                # EQ. Params: [In, In, Out]. Len: 4
                params = self._get_parameters(3)
                a = self._resolve_parameter(params[0])
                b = self._resolve_parameter(params[1])
                if a == b:
                    self._write_parameter(params[2], 1)
                else:
                    self._write_parameter(params[2], 0)
                self._next(4)
            elif opcode == 9:
                # Adjust the relative base. Params: [In]. Len: 2
                params = self._get_parameters(1)
                a = self._resolve_parameter(params[0])
                self.relative_base += a
                self._next(2)
            else:
                raise Exception(f'Error. Unable to process op ({opcode}) at [{self.instruction_pointer}]')
            self.cycle += 1