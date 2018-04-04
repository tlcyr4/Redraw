from django.shortcuts import redirect
from django.conf import settings
from RedrawApp import views

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        views.logView(request)
        response = self.get_response(request)
        print(request.path)
        # Code to be executed for each request/response after
        # the view is called.
        #print(str(request.user) == "")
        #if (str(request.user) == "dkchae"):
        #    print(request.user)
        #    print(request.path)
        #    if not request.user.is_authenticated:
        #        return redirect('accounts/login')
        return response