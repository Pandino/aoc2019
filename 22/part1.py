import re
from functools import partial, reduce

def reverse_deal_into_new_stack(stack_size, position):
    return stack_size - position - 1

def reverse_cuts(stack_size, cuts_n, position):
    last_cut_size = stack_size - cuts_n
    if position < last_cut_size:
        return position + cuts_n
    else:
        return position - last_cut_size

def cuts(stack_size, cuts_n, position):
    if cuts_n > 0:
        last_cut_size = stack_size - cuts_n
    else:
        last_cut_size = -cuts_n
        cuts_n = stack_size + cuts_n
    if position < cuts_n:
        return position + last_cut_size
    else:
        return position - cuts_n

def reverse_deal_with_inc(stack_size, increment, position):
    modinv = pow(increment, -1, stack_size)
    return (position * modinv) % stack_size

def deal_with_inc(stack_size, increment, position):
    return (position * increment) % stack_size

def compose2(f, g):
    return lambda x: f(g(x))


if __name__ == "__main__":
    new_stack_rc = re.compile(r'deal into new stack')
    cut_rc = re.compile(r'cut (-?\d+)')
    inc_rc = re.compile(r'deal with increment (\d+)')

    stack_size = 10007
    shuffle = lambda x:x

    rev_new_stack_func = partial(reverse_deal_into_new_stack, stack_size)
    steps = 0
    with open('22/input') as f:
        for step in f:
            match = new_stack_rc.match(step)
            if match:
                shuffle = compose2(rev_new_stack_func, shuffle)
                steps += 1
            else:
                match = cut_rc.match(step)
                if match:
                    rev_cut_func = partial(cuts, stack_size, int(match.group(1)))
                    shuffle = compose2(rev_cut_func, shuffle)
                    steps += 1
                else:
                    match = inc_rc.match(step)
                    if match:
                        rev_inc_func = partial(deal_with_inc, stack_size, int(match.group(1)))
                        shuffle = compose2(rev_inc_func, shuffle)
                        steps += 1
    
    print(shuffle(2019))
    
