start = 387638
imax = 919123

class OutOfBoundException(Exception):
    pass

def num_to_int(number):
    return int(''.join([str(n) for n in number]))

def int_to_num(integer):
    return [int(i) for i in str(integer)]

def is_valid(number):
    ''' Verify that number is a valid password. Number is a list ot tuple of integers '''
    if len(number) != 6:
        raise Exception(f'Not a 6 digit number: {num_to_int(number)}')

    int_number = num_to_int(number)

    if int_number < start or int_number > imax:
        raise OutOfBoundException()

    counts = list()
    counter = 1
    prev_digit = number[0]
    for digit in number[1:]:
        if prev_digit > digit:
            return False
        if prev_digit == digit:
            counter += 1
        else:
            counts.append(counter)
            counter = 1
        prev_digit = digit
    counts.append(counter)

    if 2 in counts:
        return True
    return False

total = 0

for i in range(start, imax+1):
    current = int_to_num(i)
    if is_valid(current):
        print(i, current)
        total += 1

print(total)