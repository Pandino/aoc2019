from intcode import cpu
from blessed import Terminal

def import_code(filename):
    code = list()
    with open(filename) as f:
        for line in f:
            instructions = [int(i) for i in line.strip().split(',')]
            code.extend(instructions)
    return instructions

class Arcade():
    def __init__(self, code):
        self.cpu = cpu.Cpu(code)
        self.output_buffer = list()
        self.tile_map = (' ', '#', '&', '_', 'o')
        self.terminal = Terminal()
        print(self.terminal.clear, end='')

    def run(self):
        while True:
            state = self.cpu.run()
            if state[0] == 0:
                break
            elif state[0] == 1:
                raise NotImplementedError()
            elif state[0] == 2:
                self.output_buffer.append(state[1])
                if len(self.output_buffer) >= 3:
                    x, y, tile = self.output_buffer[0:3]
                    self.update_screen(x, y, tile)
                    self.output_buffer = list()

    def update_screen(self, x, y, tile):
        print(self.terminal.move(y, x) + self.tile_map[tile], end='')

if __name__ == '__main__':
    code = import_code('13/input.int')
    game = Arcade(code)
    game.run()
    print()