pic_size = (25, 6)

def get_input(filename):
    with open(filename) as f:
        return f.readlines()[3]

class Layer():
    '''The Layer class use indexes to determine the starting and ending point of a picture layer
    '''
    def __init__(self, picture, start, end, label=None):
        self.picture = picture
        self.start = start
        self.end = end
        self.label = label
        self.stats = dict()

    def data(self):
        for i in range(self.start, self.end):
            yield picture[i]

    def get_pixel(self, pos):
        if self.start + pos > self.end:
            raise Exception(f'Layer {self.label} out of bounds. Pos: {pos}')
        return picture[self.start + pos]

    def count(self, value):
        '''Populate the self.stat dict'''
        if value not in self.stats:
            for i in self.data():
                if i in self.stats:
                    self.stats[i] += 1
                else:
                    self.stats[i] = 1
        return self.stats[value]

    def checksum(self):
        return self.count('1') * self.count('2')


picture = get_input('08/input')
layers = list()

index = 0
layer_size = pic_size[0] * pic_size[1]

while index < len(picture):
    layers.append(Layer(picture, index, index + layer_size, label=str(len(layers)+1)))
    index += layer_size

# find the layer with fewest 0s

low_layer = layers[0]
for layer in layers:
    zeroes = layer.count('0')
    if zeroes < low_layer.count('0'):
        low_layer = layer

print(f'Layer {low_layer.label} has {low_layer.count("0")} zeroes. Checksum = {low_layer.checksum()}')

for y in range(pic_size[1]):
    for x in range(pic_size[0]):
        position = y * pic_size[0] + x
        for layer in layers:
            pixel = layer.get_pixel(position)
            if pixel == '2':
                continue
            elif pixel == '1':
                print('*', end='')
                break
            elif pixel == '0':
                print(' ', end='')
                break
    print()