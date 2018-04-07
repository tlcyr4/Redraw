from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

# Create your models here. 

class Draw(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    res_college = models.BooleanField()
    upperclass = models.BooleanField()


class Building(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    number = models.CharField(max_length=4,unique=True)
    coordinates = JSONField()
    draw = models.ManyToManyField(Draw)

class Floor(models.Model):
    building = models.ForeignKey(Building,on_delete=models.CASCADE)
    level = models.CharField(max_length=2)
    floorplan = models.TextField()

class Room(models.Model):
    # my key
    room_id = models.AutoField(primary_key=True)
    draws_in = models.ForeignKey(Draw,null=True,on_delete=models.SET_NULL)
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    number = models.CharField(max_length=6)
    sqft = models.PositiveSmallIntegerField()
    num_occupants = models.PositiveSmallIntegerField()
    num_rooms = models.PositiveSmallIntegerField()
    sub_free = models.NullBooleanField(null = True)
    ada = models.NullBooleanField("Americans with Disabilities Act Compliance",null=True)

    # collapsed from past draw model
    draw_rank = ArrayField(models.IntegerField(null=True),size=5)
    size_rank = ArrayField(models.IntegerField(null=True),size=5)
    
    # collapsed from polygons model
    polygons = JSONField(null=True)

class User(models.Model):
    netid = models.CharField(max_length=30,primary_key=True)
    # should be many to many
    # keep equal to group_id
    groups = ArrayField(models.IntegerField(null=True),size=5)
    # should be many to many
    # should always be equal to room_id
    favorites = ArrayField(models.IntegerField(null=True),size=20)
    
class Group(models.Model):
    drawing_in = models.ForeignKey(Draw,null=True,on_delete=models.SET_NULL)
    draw_time = models.DateTimeField()
    # should be many to many
    # should be netids
    members = ArrayField(models.CharField(max_length=30))




# post launch
# class PlanUserRoom(models.Model):
#     plan = models.ForeignKey('Plan',on_delete=models.CASCADE)
#     occupant = models.ForeignKey('User', on_delete=models.CASCADE)
#     room = models.ForeignKey('Room')

# class Plan(models.Model):
#     group = models.ForeignKey('Group')