from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .models import Profile
import base64

def index(request):
    profiles = Profile.objects.all()
    context = { "profiles": profiles }
    return render(request, "dashboard/index.html", context)

def profile(request, id):
    profile = Profile.objects.get(pk=id)
    context = { "profile": profile }
    return render(request, "dashboard/profile.html", context)

def image(request, name):
    file = "{}/img/{}".format(settings.MEDIA_ROOT, name)
    image = open(file, 'rb').read()
    return HttpResponse(image)

def gpx(request, id):
    print("REQ -->", request)
    print("NAME -->", id)
    context = {
        "id": id
    }
    return render(request, "dashboard/gpx.html", context)
