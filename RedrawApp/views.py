from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def logView(request):
	print(request.user)
	print("HI")
	return redirect('accounts/login')