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
from os import path

campus = json.load(open("ranktree.json","r"))
buildings = json.load(open("buildings.json","r"))

bldg2num = {}
for num in buildings:
    bldg2num[standardized(buildings[num]['name'])]=num
# print(bldg2num)
total = 0
for buildingname in campus:
    building = campus[buildingname]
    for floornum in building:
        fn = "polygons/"+bldg2num[standardized(buildingname)]+"-"+floornum+".json"
        if not path.isfile(fn):
            continue
        polygons = json.load(open(fn,"r"))
        floor = building[floornum]
        for room in floor:
            floor[room]['polygons'] = []
            for polygon in polygons:
                if polygon['number'] in room:
                    total += 1
                    origin = polygon['origin']
                    points = []
                    for point in polygon['polygon']:
                        points.append([point[0][0]+origin[0],point[0][1]+origin[1]])
                    floor[room]['polygons'].append(points)
json.dump(campus,open("merged.json","w"))
print(total)