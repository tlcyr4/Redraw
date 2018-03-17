import json
f = open("conventions.txt", "r")
line = ""
while line.strip("\n") != ("=" * 80):
	line = f.readline() #skip this documentation section
conventions = [line.strip("\n").split("\t") for line in f]

def standardized(name):
    found = False
    for c in conventions:
        if name in c:
            found = True    
            return c[0]
            break
    if not found:
        print "Error: Unknown Term: " + name
    return name


data = open('Room_Draw_11.txt', 'U')
description = data.readline()
line = data.readline()
if line == '':
    print 'Empty file'

campus = {}
while line != '':
    tokens = line.split()
    if len(tokens) == 0:
        break
    time = ' '.join(tokens[:5])
    tokens = tokens[5:]
    roomnum = tokens.pop(0)
    building = tokens.pop(0)
    if tokens[0] == 'OSBORN':
        building += ' ' + tokens.pop(0)
    building = building.upper()
    if building == 'WENDELL':
        if 'B' in roomnum:
            building = 'WENDELL B'
        if 'C' in roomnum:
            building = 'WENDELL C'
    if building == 'FORBES':
        if 'A' in roomnum:
            building = 'FORBES ADDITION'
        else:
            building = 'FORBES MAIN INN'
    if building == 'BAKER':
        if 'E' in roomnum:
            building = 'BAKER E'
        if 'S' in roomnum:
            building = 'BAKER S'

    building = standardized(building)


    occupancy = int(tokens.pop(0))
    draw = tokens.pop(0).upper()
    if tokens[0] == 'College':
        tokens.pop(0)
    sqft = int(tokens.pop(0))
    numrooms = int(tokens.pop(0))
    # print tokens
    if len(tokens) > 1 and tokens[1] ==  'bathroom':
        bathroom = tokens.pop(0)
        tokens.pop(0)
        if bathroom == 'Shared':
            bathroom += ' ' + tokens.pop(0)
    else:
        bathroom = 'Public'
    # print tokens
    floornum = int(tokens.pop(0))
    features = ' '.join(tokens)
    # print features
    if draw not in campus:
        campus[draw] = {}
    if building not in campus[draw]:
        campus[draw][building] = []
    if len(campus[draw][building]) <= floornum:
        campus[draw][building].extend([None] * (1 + floornum - len(campus[draw][building])))
    if campus[draw][building][floornum] == None:
        campus[draw][building][floornum] = {}
    floor = campus[draw][building][floornum]
    room = {}
    floor[roomnum] = room
    room['occupancy'] = occupancy
    room['bathroom'] = bathroom
    room['sqft'] = sqft
    room['numrooms'] = numrooms

    
    room['sub-free'] = ('Substance free room' in features)
    if room['sub-free']:
        features = features.replace('Substance free room', '')
    room['ada'] = 'ADA Accessible' in features
    if room['ada']:
        features = features.replace('ADA Accessible', '')

    room['bi-level'] = ('Bi-level room' in features)
    if room['bi-level']:
        features = features.replace('Bi-level room', '')

    room['connecting'] = ('Connecting single' in features)
    if room['connecting']:
        features = features.replace('Connecting single', '')

    room['features'] = features


    line = data.readline()

out = open('rooms.json', 'w')
json.dump(campus, out)