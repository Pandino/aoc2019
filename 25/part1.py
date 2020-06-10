from intcode.ascii import Ascii

if __name__ == "__main__":
    with open('25/input.int') as f:
        code = [int(i) for i in f.readline().split(',')]
    terminal = Ascii(code)
    terminal.run()