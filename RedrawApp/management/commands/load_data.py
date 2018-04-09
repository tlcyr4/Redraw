# from csv import DictReader
import json
from datetime import datetime
from glob import glob
from PIL import Image

from django.core.management import BaseCommand

from RedrawApp.models import Floor, Building, Draw, Room
from pytz import UTC



f = open("data/aliases.txt", "r")
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

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

years = 5
class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from pet_data.csv into our Floor model"

    def handle(self, *args, **options):
        # load draws
        print("Loading Draws")
        f = open("data/draws.txt", "r")
        draws = {}
        draw_models = {}
        for line in f:
            tokens = line.strip("\n").split("\t")
            draws[tokens[0].upper()] = list(map(standardized, tokens[1:]))
        res_colleges = ["BUTLER","FORBES","MATHEY","ROCKEFELLER","WHITMAN","WILSON"]
        if Draw.objects.exists():
            Draw.objects.all().delete()
        for draw in draws.keys():
            res_college = draw in res_colleges
            upperclass = draw not in ["FORBES","ROCKEFELLER","WILSON"]
            d = Draw(name = draw, res_college = res_college, upperclass = upperclass)
            d.save()
            draw_models[draw] = d


        print("Loading Buildings and Floors")
        import json
        buildings = json.load(open("data/buildings.json", "r"))
        polygons = json.load(open("data/building_polygons.json","r"))
        rooms = json.load(open("data/merged.json","r"))
        dimensions = json.load(open("data/dimensions.json"))
        from os import path
        import base64
        # load buildings and floors
        if Building.objects.exists():
            Building.objects.all().delete()
        if Floor.objects.exists():
            Floor.objects.all().delete()
        for buildingnum in buildings.keys():

            building = buildings[buildingnum]
            name = standardized(building["name"])
            coordinates = None
            for polygon in polygons:
                if polygon["properties"]["id"] == buildingnum:
                    coordinates = json.dumps(polygon["geometry"]["coordinates"])
            building_model = Building(name=name,coordinates=coordinates,number=buildingnum)
            # print(building_model.name,building_model.number)
            building_model.save()
            # handle many to many
            mydraws = []
            for draw in draws.keys():
                if name in draws[draw]:
                    mydraws.append(draw_models[draw])
                    pass
            
            # print(name,coordinates[0][:1],mydraws)
            for draw in mydraws:
                building_model.draw.add(draw)
                pass

            floors = building["floors"]
            for floor in floors:
                fn = buildingnum + "-" + floor 
                floor_model = Floor(building=building_model,dimensions=dimensions[fn],level=floor)
                floor_model.save()
                if name not in rooms:
                    continue
                if floor not in rooms[name]:
                    continue
                for room in rooms[name][floor].values():
                    draw = room["draw"].replace(" COLLEGE","")
                    # r_building = standardized(room["buildingname"])
                    # floor = "0" + room["floor"]
                    num_rooms = int(room["numrooms"])
                    sub_free = None # don't have data
                    num_occupants = int(room["occ"])
                    sqft = int(room["sqft"])
                    number = room["number"]
                    draw_rank = list(map(int, room["overallrank"])) + [None] * (years - len(room["overallrank"]))
                    size_rank = list(map(int, room["sizerank"])) + [None] * (years - len(room["sizerank"]))
                    r_polygons = json.dumps(room['polygons'])
                    ada = None
                    # print(draw,name,floor,number,sqft,num_occupants,num_rooms,sub_free,ada,draw_rank,size_rank,r_polygons)
                    room_model = Room(
                    draws_in=draw_models[draw],
                    floor = floor_model,
                    number = number,
                    sqft = sqft,
                    num_occupants = num_occupants,
                    num_rooms = num_rooms,
                    sub_free = sub_free,
                    ada = ada,
                    draw_rank = draw_rank,
                    size_rank = size_rank,
                    polygons = r_polygons 
                    )
                    # print(room_model.sqft)
                    room_model.save()