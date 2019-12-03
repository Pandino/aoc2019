import sys

def distance(p1, p2):
    '''Calculate Manhattan distance between two points p1 and p2.
    Point coordinates are represented as interger tuples, i.e. (x, y)
    '''

    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)

def is_crossing(a1, a2, b1, b2):
    '''Return False if the two segments (a1, a2), (b1, b2) do not intersect, if they
    intersect, return the tuple intersection point.
    Throw an exception if the segments intersect in multiple points.
    '''

    xa1, ya1 = a1
    xa2, ya2 = a2
    xb1, yb1 = b1
    xb2, yb2 = b2

    left = max(min(xa1, xa2), min(xb1, xb2))
    right = min(max(xa1, xa2), max(xb1, xb2))

    bottom = max(min(ya1, ya2), min(yb1, yb2))
    top = min(max(ya1, ya2), max(yb1, yb2))

    if (left > right) or (bottom > top):
        return False
    
    if (left == right) and (bottom == top):
        print(f'Found! {left}, {top}')
        return (left, bottom)

    print(left, bottom, right, top)
    raise Exception('Multipoint segment intersection.')

def move(start, to):
    '''Return next coordinate point'''

    direction = to[0]
    distance = int(to[1:])

    if direction == 'U':
        return (start[0], start[1] + distance)
    if direction == 'D':
        return (start[0], start[1] - distance)
    if direction == 'R':
        return (start[0] + distance, start[1])
    if direction == 'L':
        return (start[0] - distance, start[1])

    raise Exception('Unrecognized instruction ', to)
        

intersections = list()

wires = list()
with open('input') as f:
    for line in f:
        wires.append(line)

wire_a_moves = wires[0].split(',')
wire_b_moves = wires[1].split(',')

a = (0, 0)
b = (0, 0)

for a_move in wire_a_moves:
    a_next = move(a, a_move)
    for b_move in wire_b_moves:
        b_next = move(b, b_move)
        print(a, a_next, b, b_next)
        c = is_crossing(a, a_next, b, b_next)
        if c:
            intersections.append(c)
        b = b_next
    a = a_next
    b = (0, 0)

intersections.remove((0, 0))
if len(intersections) == 0:
    print('No intersections found')
    sys.exit()

distances = list()
for cross in intersections:
    distances.append(distance((0, 0), cross))
print(f'CLosest intersection: {min(distances)}')




