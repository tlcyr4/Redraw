import json

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
    occupancy = tokens.pop(0)
    draw = tokens.pop(0)
    # print tokens
    if tokens[0] == 'College':
        draw = ' '.join((draw, tokens.pop(0)))
    sqft = tokens.pop(0)
    numrooms = tokens.pop(0)
    # print tokens
    if len(tokens) > 1 and tokens[1] ==  'bathroom':
        bathroom = tokens.pop(0)
        tokens.pop(0)
        if bathroom == 'Shared':
            bathroom = ' '.join((bathroom, tokens.pop(0)))
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