class OrbitObject():
    def __init__(self, name, orbit=None):
        self.name = name
        self.orbit = orbit

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<OrbitObject> {self.name} orbiting arount {self.orbit}'

    def __str__(self):
        if self.orbit is not None:
            return f'{self.orbit.name}){self.name}'
        else:
            return self.name

def get_object(objects, name):
    for object in objects:
        if object.name == name:
            return object
    return None

def count_orbits(obj, destination=None):    
    if destination is not None and destination == obj:
        return 0
    if obj.orbit is None:
        return 0
    return 1 + count_orbits(obj.orbit, destination)

def get_path(obj, path=None):
    if path is None:
        path = list()
    if obj.orbit is None:
        return [obj]
    return path.append(get_path(obj.orbit, path))

if __name__ == '__main__':

    objects = set()
    line_count = 0
        
    with open('06/test.txt') as f:
        for line in f:
            line_count += 1
            obj_a, obj_b = line.strip().split(')')[0:2]
            parent = get_object(objects, obj_a)
            if parent is None:
                parent = OrbitObject(obj_a)
                objects.add(parent)
            orbiter =  get_object(objects, obj_b)
            if orbiter is not None:
                if orbiter.orbit is not None:
                    raise Exception(f'Found a double orbit object: {orbiter}')
                orbiter.orbit = parent
            else:
                orbiter = OrbitObject(obj_b, parent)
                objects.add(orbiter)
    
    print(f'Processed {line_count} lines and found {len(objects)} objects')

    #print(sum([count_orbits(object) for object in objects]))

    #print(count_orbits(get_object(objects, 'H'), get_object(objects, 'B')))
    
    h = get_object(objects,'H')
    print(get_path(h))
        
