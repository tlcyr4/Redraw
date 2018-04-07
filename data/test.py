# from RedrawApp.models import Floor, Draw, Building

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
years = 5
import json
rankings = json.load(open("merged.json","r"))
for room in rankings:
    draw = room["draw"].replace(" COLLEGE","")
    building = standardized(room["buildingname"])
    floor = "0" + room["floor"]
    num_rooms = int(room["numrooms"])
    sub_free = None # don't have data
    num_occupants = int(room["occ"])
    sqft = int(room["sqft"])
    number = room["number"]
    draw_rank = list(map(float, room["overallrank"])) + [None] * (years - len(room["overallrank"]))
    size_rank = list(map(float, room["sizerank"])) + [None] * (years - len(room["sizerank"]))
    polygons = json.dumps(room['polygons'])
    ada = None
    print(draw,building,floor,number,sqft,num_occupants,num_rooms,sub_free,ada,draw_rank,size_rank,polygons)
    # # room_model = Room(
    #     draws_in=draw,
    #     floor = floor,
    #     number = number,
    #     sqft = sqft,
    #     num_occupants = num_occupants,
    #     num_rooms = num_rooms,
    #     sub_free = sub_free,
    #     ada = ada,
    #     draw_rank = draw_rank,
    #     size_rank = size_rank,
    #     polygons = polygons 
    #     )
