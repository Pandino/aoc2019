from intcode import cpu
from blessed import Terminal
from time import sleep

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
                with self.terminal.cbreak():
                    val = self.terminal.inkey(timeout=0)
                    if val == 'a':
                        self.cpu.input(-1)
                    elif val == 'd':
                        self.cpu.input(1)
                    elif val == 'q':
                        break
                    else:
                        self.cpu.input(0)
            elif state[0] == 2:
                self.output_buffer.append(state[1])
                if len(self.output_buffer) == 3:
                    x, y, tile = self.output_buffer
                    self.update_screen(x, y, tile)
                    self.output_buffer = list()

    def update_screen(self, x, y, tile):
        if x == -1:
            print(self.terminal.move(0, 0) + str(tile))
        else:
            y += 1
            print(self.terminal.move(y, x) + self.tile_map[tile], end='')

if __name__ == '__main__':
    code = import_code('13/input.int')
    code[0] = 2
    game = Arcade(code)
    game.run()
    print()