from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Building, Room, Floor, Draw, Profile
import json

@login_required
def query(request):
	queries = request.GET.dict()

	# remove empty queries
	queries = {k:v for k,v in queries.items() if v != ""}

	if 'building' in queries:
		queries['floor__building__name'] = queries.pop('building').replace("%20"," ")
	if 'level' in queries:
		if queries['level'].isdigit():
			queries['level'] = queries['level'].zfill(2)
		queries['floor__level'] = queries.pop('level')
	if 'draw' in queries:
		queries['draws_in_id__name'] = queries.pop('draw').upper()
	
	queried = Room.objects.filter(**queries).order_by('floor__level')
	results = list(queried.values())

	for room in results:
		room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
		room['level'] = Floor.objects.get(id=room['floor_id']).level[-1]
		room['draws_in'] = Draw.objects.get(id=room['draws_in_id']).name.capitalize()
		room['building_name'] = Floor.objects.get(id=room['floor_id']).building.name
		if room['num_rooms'] == None:
			room['num_rooms'] = "Unknown"
	return HttpResponse(json.dumps(results), content_type='application/json')

@login_required
def get_floorplan(request):

	building_num = request.GET.get('building','')
	level = request.GET.get('level', '')
	if level == '' or building_num == '':
		return HttpResponseBadRequest()
	
	if level.isdigit():
		level = level.zfill(2)
	filename = 'data/floorplans/' + building_num + '-' + level + '.png'
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
		rooms = list(Room.objects.filter(pk__in=trimmed).values())
		for room in rooms:
			room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
			room['level'] = Floor.objects.get(id=room['floor_id']).level[-1]
			room['draws_in'] = Draw.objects.get(id=room['draws_in_id']).name.capitalize()
			room['building_name'] = Floor.objects.get(id=room['floor_id']).building.name
		return HttpResponse(json.dumps(rooms), content_type="application/json")
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
	
	rooms = list(Room.objects.filter(pk__in=trimmed).values())
	for room in rooms:
		room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
		room['level'] = Floor.objects.get(id=room['floor_id']).level[-1]
		room['draws_in'] = Draw.objects.get(id=room['draws_in_id']).name
		room['building_name'] = Floor.objects.get(id=room['floor_id']).building.name
		if room['num_rooms'] == None:
			room['num_rooms'] = "Unknown"
	return HttpResponse(json.dumps(rooms), content_type="application/json")
