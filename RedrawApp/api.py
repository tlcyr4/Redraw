from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Building, Room
import json

@login_required
def query(request):
	queries = request.GET.dict()
	if 'building' in queries:
		queries['floor__building'] = queries.pop('building')
	if 'level' in queries:
		queries['floor__level'] = queries.pop('level')
	result = Room.objects.filter(**queries)

	return HttpResponse(json.dumps(list(result.values())), content_type='application/json')

@login_required
def get_floorplan(request):

	room_id = request.GET.get('room_id','')
	if room_id == '':
		return HttpResponseBadRequest()
	floor = Room.objects.get(room_id=room_id).floor
	number = floor.building.number
	level = floor.level
	filename = 'data/floorplans/' + number + '-' + level + '.pdf'
	floorplan = open(filename,'rb').read()
	return HttpResponse(floorplan, content_type='application/pdf')
