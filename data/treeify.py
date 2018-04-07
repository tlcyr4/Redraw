f = open("aliases.txt", "r")
line = ""
while line.strip("\n") != ("=" * 80):
	line = f.readline() #skip this documentation section
conventions = [line.strip("\n").split("\t") for line in f]

def standardized(name):
    name = name.upper()
    name = name.replace(" HALL", "")
    name = name.replace("CLASS OF ", "")
    name = name.replace(" COLLEGE", "")
    found = False
    for c in conventions:
        if name in c:
            found = True    
            return c[0]
    if not found:
        print("Error: Unknown Term: ", name)
    return name
    
import json
rooms = json.load(open("rankings.json","r"))
campus = {}

for room in rooms:
    if room['buildingname'] not in campus:
        campus[standardized(room['buildingname'])] = {}
    building = campus[standardized(room['buildingname'])]
    if room['floor'].isnumeric():
        room['floor'] = "0" + room['floor']
    if room['floor'] not in building:
        building[room['floor']] = {}
    floor = building[room['floor']]
    floor[room['number']]= room

json.dump(campus,open("ranktree.json","w"))