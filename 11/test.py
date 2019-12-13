rotation_matrixes = ( ((0, -1), (1, 0)),
                      ((0, 1), (-1, 0)) )

vector = (0, 1)

for turn_matrix in rotation_matrixes:
    direction = [ sum(a * b for a, b in zip(vector, rotation_column)) for rotation_column in zip(*turn_matrix) ]
    print(direction)