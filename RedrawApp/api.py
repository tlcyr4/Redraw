from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Building, Room, Floor, Draw, Profile
import json

@login_required
def query(request):
	queries = request.GET.dict()
	if 'building' in queries:
		print("foo")
		queries['floor__building__name'] = queries.pop('building').replace("%20"," ")
	if 'level' in queries:
		queries['floor__level'] = queries.pop('level')
	queried = Room.objects.filter(**queries).order_by('floor__level')
	results = list(queried.values())

	for room in results:
		room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
		room['level'] = Floor.objects.get(id=room['floor_id']).level
		room['draws_in'] = Draw.objects.get(id=room['draws_in_id']).name
	return HttpResponse(json.dumps(results), content_type='application/json')

@login_required
def get_floorplan(request):

	room_id = request.GET.get('room_id','')
	if room_id == '':
		return HttpResponseBadRequest()
	floor = Room.objects.get(room_id=room_id).floor
	number = floor.building.number
	level = floor.level
	filename = 'data/floorplans/' + number + '-' + level + '.png'
	floorplan = open(filename,'rb').read()
	return HttpResponse(floorplan, content_type='image/png')

@login_required
def favorites(request):
	netid = str(request.user)
	room_id = int(request.GET.get('room_id', '0'))
	profile = Profile.objects.get(user__username=netid)
	favorites = profile.favorites
	length = len([fav for fav in favorites if fav != None])
	if Room.objects.filter(room_id=room_id).count() == 0:
		trimmed = [fav for fav in favorites if fav != None]
		for room in trimmed:
			room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
			room['level'] = Floor.objects.get(id=room['floor_id']).level
			room['draws_in'] = Draw.objects.get(id=room['draws_in_id']).name
		return HttpResponse(json.dumps(trimmed), content_type="application/json")
	if room_id not in favorites:
		if favorites[-1] != None:
			return HttpResponseBadRequest("overflow")
		else:
			favorites[length] = room_id
	else:
		index = favorites.index(room_id)
		favorites[index] = favorites[length - 1]
		favorites[length - 1] = None
	profile.save()
	trimmed = [fav for fav in favorites if fav != None]
	for room in trimmed:
		room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
		room['level'] = Floor.objects.get(id=room['floor_id']).level
		room['draws_in'] = Draw.objects.get(id=room['draws_in_id']).name
	rooms = list(Room.objects.filter(pk__in=trimmed).values())
	return HttpResponse(json.dumps(rooms), content_type="application/json")

