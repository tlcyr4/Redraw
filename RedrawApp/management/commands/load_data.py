# from csv import DictReader
import json
from datetime import datetime
from os import path

from django.core.management import BaseCommand

from RedrawApp.models import Floor, Building, Draw, Room
from pytz import UTC






years = 5
class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data into our Floor model"

    def handle(self, *args, **options):
        real = True
        
        RES_COLLEGES = ["BUTLER","FORBES","MATHEY","ROCKEFELLER","WHITMAN","WILSON"]
        NOT_UPPERCLASS = ["FORBES","ROCKEFELLER","WILSON"]
        
        if real and Draw.objects.exists():
            print("Deleting Old Draws")
            Draw.objects.all().delete()
        
        print("Loading Draws")
        
        tokenses = [line.strip("\n").split("\t") for line in open("data/draws.txt", "r")]
        draws = {tokens[0].upper():tokens[1:] for tokens in tokenses}
        draw_models = {draw: Draw(
            name=draw,
            res_college = draw in RES_COLLEGES,
            upperclass = draw not in NOT_UPPERCLASS
            ) for draw in draws}
        print(draw_models)
        if real:
            [draw_model.save() for draw_model in draw_models.values()]

        buildings = json.load(open("data/buildings_clean.json", "r"))
        rooms = json.load(open("data/AVAIL18.json","r"))
        dimensions = json.load(open("data/dimensions.json"))

        # load buildings and floors
        if real and Building.objects.exists():
            print("Deleting Old Buildings")
            Building.objects.all().delete()
        print("Loading Buildings")
        building_models = [
            Building(
                coordinates =  json.dumps(building["polygons"]) if "polygons" in building else None,
                number = buildingNum,
                name=building["name"]
            )
            for buildingNum, building in buildings.items()
        ]
        print(building_models)
        if real:
            [building_model.save() for building_model in building_models]
            [[building_model.draw.add(model) for draw,model in draw_models.items() if building_model.number in draws[draw]] for building_model in building_models]

        if real and Floor.objects.exists():
            print("Deleting Old Floors")
            Floor.objects.all().delete()
        print("Loading Floors")
        floors = [[Floor(
            building = building_model,
            dimensions = dimensions[building_model.number + "-" + floor],
            level=floor
        ) for floor in buildings[building_model.number]["floors"]] 
        for building_model in building_models]
        floors = [floor for building in floors for floor in building]
        
        if real:
            [floor.save() for floor in floors]

        floors_dict = {floor.building.number + "-" + floor.level: floor for floor in floors}
        # print(floors_dict)

        if real and Room.objects.exists():
            print("Deleting Old Rooms")
            Room.objects.all().delete()
        print("Loading Rooms")
        room_models = [
            Room(
                num_rooms =     int(room["num_rooms"]) if room["num_rooms"] != "" else None,
                sub_free =      room["sub_free"] == "Yes",
                num_occupants = int(room["occ"]),
                sqft =          int(room["sqft"]),
                number =        room["number"],
                draw_rank =     list(map(int, room["draw_rank"])) + [None] * (years - len(room["draw_rank"])),
                size_rank =     list(map(int, room["size_rank"])) + [None] * (years - len(room["size_rank"])),
                polygons =      json.dumps(room['polygons']),
                floor = floors_dict[room["building"] + "-" + ("A" if room["level"] == "A" else room["level"].zfill(2))],
                draws_in = draw_models[room["draw"].upper()]
            ) for room in rooms
        ]
        if real:
            [room_model.save() for room_model in room_models]