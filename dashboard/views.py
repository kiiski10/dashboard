from django.shortcuts import render
from .models import Profile

def index(request):
    profiles = Profile.objects.all()
    context = { "profiles": profiles }
    return render(request, "dashboard/index.html", context)

def profile(request, id):
    profile = Profile.objects.get(pk=id)
    context = { "profile": profile }
    return render(request, "dashboard/profile.html", context)

def image(request, id):
    context = {
        "id": id
    }
    return render(request, "dashboard/image.html", context)

def gpx(request, id):
    print("REQ -->", request)
    print("NAME -->", id)
    context = {
        "id": id
    }
    return render(request, "dashboard/gpx.html", context)
