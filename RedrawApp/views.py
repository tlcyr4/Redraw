from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# Create your views here.
def indexMap(request):
	# print(request.user)
	print(request.user.is_authenticated)
	return TemplateView.as_view(template_name='index.html')