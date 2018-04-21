from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Building, Room, Floor
import json

@login_required
def query(request):
	queries = request.GET.dict()
	if 'building' in queries:
		queries['floor__building'] = queries.pop('building')
	if 'level' in queries:
		queries['floor__level'] = queries.pop('level')
	queried = Room.objects.filter(**queries)
	results = list(queried.values())

	for room in results:
		room['dimensions'] = Floor.objects.get(id=room['floor_id']).dimensions
		room['level'] = Floor.objects.get(id=room['floor_id']).level
	return HttpResponse(json.dumps(results), content_type='application/json')

@login_required
def get_floorplan(request):

	room_id = request.GET.get('room_id','')
	if room_id == '':
		return HttpResponseBadRequest()
	floor = Room.objects.get(room_id=room_id).floor
	number = floor.building.number
	level = floor.level
	filename = 'data/floorplans/' + number + '-' + level + '.jpg'
	floorplan = open(filename,'rb').read()
	return HttpResponse(floorplan, content_type='image/jpg')
