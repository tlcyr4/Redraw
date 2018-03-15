import json

data = open('Room_Draw_11.txt', 'U')
description = data.readline()
line = data.readline()
if line == '':
    print 'Empty file'

campus = {}
i = 0
while line != '':
    i += 1
    tokens = line.split()
    if len(tokens) == 0:
        break
    time = ' '.join(tokens[:5])
    tokens = tokens[5:]
    roomnum, building, occupancy, draw = tokens[:4]
    tokens = tokens[4:]
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
    floor = tokens.pop(0)
    features = ' '.join(tokens)
    print features



    line = data.readline()