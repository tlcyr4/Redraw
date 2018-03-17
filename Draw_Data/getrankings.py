import pickle
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

d11 = pickle.load(open('Room_Draw_11.pkl', 'r'))
d14 = pickle.load(open('Room_Draw_14.pkl', 'r'))
d16 = pickle.load(open('Room_Draw_16.pkl', 'r'))
bestinfo = json.load(open('myrooms.json', 'r'))
oldinfo = pickle.load(open('oldrooms.pkl', 'r'))
tree = json.load(open('oldrooms.json', 'r'))

missing = []

def split(building, number):
    if 'BAKER' in building.upper():
        if 'E' in number:
            return 'BAKER E'
        if 'S' in number:
            return 'BAKER S'
    if 'WENDELL' in building.upper():
        if 'B' in number:
            return 'WENDELL B'
        if 'C' in number:
            return 'WENDELL C'
    if 'FORBES' in building.upper():
        if 'A' in number:
            return 'FORBES ADDITION'
        else:
            return 'FORBES MAIN INN'
    return building

print len(d11) + len(d14) + len(d16)               

count = 0
yr = 0
for year in [d11,d14,d16]:
    yr += 1
    for room in year:
        found = False
        for other in bestinfo:
            if room[1] == other['buildingname'] and int(filter(str.isdigit, room[2])) == int(filter(str.isdigit, str(other['number']))):
                found = True
                room.append(int(other['occ']))
                room.append(bool(other['sub-free']))
        if found:
            continue
        for other in oldinfo:
            if room[1] == other['buildingname'] and int(filter(str.isdigit, room[2])) == int(filter(str.isdigit, other['number'])):
                # print 'yay'
                found = True
                room.append(int(other['occ']))
                room.append(bool(other['subfree']))
        if not found:
            # print room
            if room[1] in tree[room[0]]:
                for floor in tree[room[0]][room[1]]:
                    if floor != None and room[2] in floor.keys():
                        room.append(int(floor[room[2]]['occupancy']))
                        room.append(bool(floor[room[2]]['sub-free']))
                        found = True
        if not found:
            missing.append(room)
            # print yr

print len(missing)
# print missing

total = []
for year in [d11,d14,d16]:
    rankings = {}
    for room in year:
        if len(room) == 3:
            continue
        if room[0] not in rankings:
            rankings[room[0]] = {}
        if room[3] not in rankings[room[0]]:
            rankings[room[0]][room[3]] = 0
        if 'overall' not in rankings[room[0]]:
            rankings[room[0]]['overall'] = 0
        
        room.append(rankings[room[0]]['overall'])
        room.append(rankings[room[0]][room[3]])
        rankings[room[0]]['overall'] += 1
        rankings[room[0]][room[3]] += 1
    for room in year:
        if len(room) == 3:
            continue
        room[5] = float(room[5])/rankings[room[0]]['overall']
        room[6] = float(room[6])/rankings[room[0]][room[3]]


# print 'k'
# count = 0
# for room in d14:
#     if room[0] == 'UPPERCLASS' and len(room) > 3:
#         count += 1
# print count

for room in bestinfo:
    room['overallrank'] = []
    room['sizerank'] = []
    for year in [d11,d14,d16]:
        for r in year:
            if len(r) > 3 and room['buildingname'] == r[1] and room['draw'] == r[0] and room['number'] == r[2]:
                room['overallrank'].append(r[5])
                room['sizerank'].append(r[6])

json.dump(bestinfo, open('rankings.json', 'w'))
    




# for room in info:
#     if room['buildingname'] == 'YOSELOFF':
#         print room['number']

# print info[0]

            
# pickle.dump(d11, open('Room_Draw_11.pkl', 'w'))
# pickle.dump(d14, open('Room_Draw_14.pkl', 'w'))
# pickle.dump(d16, open('Room_Draw_16.pkl', 'w'))

# pickle.dump(info, open('roominfo.pkl', 'w'))
