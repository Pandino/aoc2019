puzzle_input = '59782619540402316074783022180346847593683757122943307667976220344797950034514416918778776585040527955353805734321825495534399127207245390950629733658814914072657145711801385002282630494752854444244301169223921275844497892361271504096167480707096198155369207586705067956112600088460634830206233130995298022405587358756907593027694240400890003211841796487770173357003673931768403098808243977129249867076581200289745279553289300165042557391962340424462139799923966162395369050372874851854914571896058891964384077773019120993386024960845623120768409036628948085303152029722788889436708810209513982988162590896085150414396795104755977641352501522955134675'
test0 = '12345678'
test1 = '03036732577212944063491565474664'
test2 = '69317163492948606335995924319873'



base_pattern = (0, 1, 0, -1)

def multiplier(pos, n):
    pos = (pos+1) // n
    return base_pattern[pos%4]

def selector(digit):
    n = 0
    mult = digit + 1
    while True:
        start = digit + 2 * n * mult
        yield slice(start, start + mult)
        n += 1


def phase(signal, iterations):
    for phase in range(iterations):
        for digit in range(len(signal)):
            digit_total = 0
            #p = pattern_iter(digit+1)
            for sum_position in range(digit, len(signal)):
                digit_total += signal[sum_position] * multiplier(sum_position, digit+1)
                print(digit)
            signal[digit] = abs(digit_total) % 10
        print(signal)
    return signal

def phase2(signal, iterations, offset):
    for phase in range(iterations):
        for digit in range(offset, len(signal)):
            new_digit = 0
            select = selector(digit)
            mult = 1
            while True:
                s = next(select)
                if s.start >= len(signal):
                    break
                new_digit += sum(signal[s]) * mult
                mult *= -1
            signal[digit] = abs(new_digit) % 10
        print(phase)
    return signal


def phase3(signal, iterations, offset):
    for phase in range(iterations):
        for digit in range(len(signal) - 2, offset - 1, -1):

            if digit > len(signal)//2 :
                signal[digit] = (signal[digit] + signal[digit + 1]) % 10
                continue

            new_digit = 0
            select = selector(digit)
            mult = 1
            while True:
                s = next(select)
                if s.start >= len(signal):
                    break
                new_digit += sum(signal[s]) * mult
                mult *= -1
            signal[digit] = abs(new_digit) % 10
        print(phase)
    return signal
        
        
        
offset = int(puzzle_input[:7])
signal = puzzle_input * 10000
result = phase3([int(i) for i in signal], 100, offset)[offset:offset+8]
print(''.join([str(i) for i in result]))