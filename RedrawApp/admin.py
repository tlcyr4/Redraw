from django.contrib import admin
from RedrawApp.models import Room, Draw, Building, Group, Profile, Floor
# Register your models here.


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    pass
