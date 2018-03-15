import json

data = open('Room_Draw_11.txt', 'U')
description = data.readline()
line = data.readline()
if line == '':
    print 'Empty file'

i = 0
while line != '' and i < 1:
    i += 1
    tokens = line.split()
    time = ' '.join(tokens[:5])
    tokens = tokens[5:]
    roomnum, building, occupancy, draw = tokens[:4]
    tokens = tokens[4:]
    if tokens[0] == 'College':
        draw = ' '.join(draw, tokens.pop(0))
    sqft, numrooms = tokens[:2]
    if tokens[1] ==  'bathroom':
        bathroom = tokens.pop(0)
        tokens.pop(0)
    else:
        bathroom = 'Public'
    floor = tokens.pop(0)
    features = ' '.join(tokens)
    



    line = data.readline()