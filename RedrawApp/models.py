from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here. 

class Draw(models.Model):
    name = models.CharField(max_length=30,unique=True)
    res_college = models.BooleanField()
    upperclass = models.BooleanField()
    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=30,unique=True)
    number = models.CharField(max_length=4,unique=True)
    coordinates = JSONField(null = True)
    draw = models.ManyToManyField(Draw)
    def __str__(self):
        return self.name + " " + self.number

class Floor(models.Model):
    building = models.ForeignKey(Building,on_delete=models.CASCADE)
    level = models.CharField(max_length=2)
    dimensions = ArrayField(models.IntegerField(), size=2)
    def __str__(self):
        return self.building.name + " " + self.level

class Room(models.Model):
    # my key
    room_id = models.AutoField(primary_key=True)
    draws_in = models.ForeignKey(Draw,null=True,on_delete=models.SET_NULL)
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    number = models.CharField(max_length=6)
    sqft = models.PositiveSmallIntegerField()
    num_occupants = models.PositiveSmallIntegerField()
    num_rooms = models.PositiveSmallIntegerField(null=True)
    sub_free = models.NullBooleanField(null = True)

    # collapsed from past draw model
    draw_rank = ArrayField(models.IntegerField(null=True),size=5)
    size_rank = ArrayField(models.IntegerField(null=True),size=5)
    
    # collapsed from polygons model
    polygons = JSONField(null=True)

    def __str__(self):
        return self.floor.building.name + "\t" + self.number

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # should be many to many
    # keep equal to group_id
    groups = ArrayField(models.IntegerField(null=True),size=5,null=True)
    # should be many to many
    # should always be equal to room_id
    favorites = ArrayField(models.IntegerField(null=True),size=20,null=True)

    def __str__(self):
        return self.netid

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Group(models.Model):
    drawing_in = models.ForeignKey(Draw,null=True,on_delete=models.SET_NULL)
    draw_time = models.DateTimeField()
    # should be many to many
    # should be netids
    members = ArrayField(models.CharField(max_length=30))

    def __str__(self):
        names = [ User.objects.get(netid=netid) for netid in list(self.members) if netid != None]
        return str(names)





# post launch
# class PlanUserRoom(models.Model):
#     plan = models.ForeignKey('Plan',on_delete=models.CASCADE)
#     occupant = models.ForeignKey('User', on_delete=models.CASCADE)
#     room = models.ForeignKey('Room')

# class Plan(models.Model):
#     group = models.ForeignKey('Group')