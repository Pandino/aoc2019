from collections import defaultdict
from heapq import heappop, heappush

start = None
stop = None

def search_labels(map):
    maze_chars = ' .#'  # AKA everything that is not a label character
    y_size = len(map)
    x_size = len(map[0].strip('\n'))

    label_positions = set()
    labels = list()

    for y in range(y_size):
        for x in range(x_size):
            if (x, y) in label_positions:
                continue
            if map[y][x] not in maze_chars:
                label_positions.add((x, y))
                label = map[y][x]
                if map[y + 1][x] not in maze_chars:
                    # Vertical label
                    label_positions.add((x, y+1))
                    label += map[y+1][x]
                    for portal_y in [y-1, y+2]:
                        if portal_y > 0 and portal_y < y_size:
                            if map[portal_y][x] == '.':
                                if portal_y == 2 or portal_y == y_size - 3:
                                    recursion = -1
                                else:
                                    recursion = 1
                                labels.append((label, x, portal_y, recursion))
                                break
                else:
                    # Horizontal label
                    label_positions.add((x+1, y))
                    label += map[y][x+1]
                    for portal_x in [x-1, x+2]:
                        if portal_x > 0 and portal_x < x_size:
                            if map[y][portal_x] == '.':
                                if portal_x == 2 or portal_x == x_size - 3:
                                    recursion = -1
                                else:
                                    recursion = 1
                                labels.append((label, portal_x, y, recursion))
                                break
    return labels

def shortest_path(maze_map, start, stop, links):
        '''Find shortest path between a and b. Returns the steps needed.
        All positions are a touple of three values: recursion level, x, y.
        '''
        
        def get_next(position):
            directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
            l, x, y = position            
            if (x, y) in links:
                r, r_x, r_y = links[(x, y)]
                if l + r >= 0:
                    yield (l+r, r_x, r_y)
            yield from ((l, x + d[0], y + d[1]) for d in directions if maze_map[y + d[1]][x + d[0]] == '.')

        def distance(a, b):
            la, _, _ = a
            lb, _, _ = b
            return (lb - la) ** 2
        
        frontier = []
        come_from = {}
        cost_to = {}
        heappush(frontier, (0, start))
        come_from[start] = None
        cost_to[start] = 0

        while len(frontier) > 0:
            current = heappop(frontier)[1]

            if current == stop:
                break

            for next_point in get_next(current):
                new_cost = cost_to[current] + 1
                if next_point not in cost_to or new_cost < cost_to[next_point]:
                    cost_to[next_point] = new_cost
                    priority = new_cost + 0 #distance(next_point, stop)
                    heappush(frontier, (priority, next_point))
                    come_from[next_point] = current
        else:
            return None
        
        return cost_to[stop]

with open('20/input.txt') as f:
    raw_map = f.readlines()
    labels = search_labels(raw_map)
    
    portals_by_label = defaultdict(list)

    # recursion is +1 if it is an inner label and -1 if it is an outer one
    for label, x, y, recursion in labels:
        if label == 'AA':
            start = (0, x, y)
        elif label == 'ZZ':
            stop = (0, x, y)
        else:
            portals_by_label[label].append((recursion, x, y))
    
    portals = dict()

    # Inner labels link to outer labels, increasing the recursion level
    # if label 1 is an inner label, portals[p1] returns (-1, outer position)
    # and vice-versa for label 2.
    for label in portals_by_label:
        (r1, x1, y1), (r2, x2, y2) = portals_by_label[label]
        portals[(x1, y1)] = (r1, x2, y2)
        portals[(x2, y2)] = (r2, x1, y1)

    print(portals)

    print(shortest_path(raw_map, start, stop, portals))

    
