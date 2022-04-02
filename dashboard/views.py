from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Profile, Location, Camera
from .forms import ProfileForm, LocationForm, CameraForm
from django.views.decorators import gzip
from django.http import StreamingHttpResponse # for LiveView
from django.forms.models import model_to_dict

import cv2
from .utilities import camera
import random

def findWebCams():
    i = 0
    arr = []
    while i < 100:
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            break
        else:
            arr.append(i)
        cap.release()
        i += 1
    return arr

webcams = findWebCams()
print("CAMERAS FOUND:")
for c in webcams:
    print("\t", c)

cameras = {}
for cam_id in webcams:
    cameras[cam_id] = camera.Camera(cam_id)
    print("CAM '{}' STARTED:{}".format(cam_id, cameras[cam_id].video.isOpened()))

mapboxAccessToken = settings.MAPBOX_ACCESS_TOKEN

def getGPSLocation():
    # import gpsd
    # gpsd.connect()
    # packet = gpsd.get_current()
    # print(packet.position())
    #
    # fake it till u make it
    lat = str(61.289 + (random.randint(-500, 500) / 99.9) )[:8]
    lon = str(28.840 + (random.randint(-500, 500) / 99.9) )[:8]
    print("GOT LOCATION:", lat, lon)
    return({"lat": lat.ljust(8, "0"), "lon": lon.ljust(8, "0")})

def editProfile(request, id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect("/ep/" + id + "/")
    else:
        profile = Profile.objects.get(pk=id)
        form = ProfileForm(model_to_dict(profile))

    return render(request, 'dashboard/edit-profile.html', {
            "mapboxAccessToken": mapboxAccessToken,
            "location": getGPSLocation(),
            "id": id,
            "form": form
        }
    )

def index(request):
    return HttpResponseRedirect("/sp/")

def externalMap(request, loc):
    loc = loc.split(",")
    zoom = loc[0]
    lat = loc[1]
    lon = loc[2]
    mapProvider = "https://openstreetmap.org/"
    mapURL = "{0}directions?from={2},{3}&to=#map={1}/{2}/{3}".format(
        mapProvider,
        zoom,
        lat,
        lon,
    )
    return HttpResponseRedirect(mapURL)

def selectProfile(request):
    profiles = Profile.objects.all()
    context = {
        "profiles": profiles,
        "location": getGPSLocation()
    }
    return render(request, "dashboard/select-profile.html", context)

def profile(request, id):
    profile = Profile.objects.get(pk=id)
    waypoints = profile.location_set.all()
    cameras = profile.cameras.all()

    context = {
        "profile": profile,
        "location": getGPSLocation(),
        "waypoints": waypoints,
        "cameras": cameras,
    }
    return render(request, "dashboard/profile.html", context)

def image(request, name):
    file = "{}/img/{}".format(settings.MEDIA_ROOT, name)
    image = open(file, 'rb').read()
    return HttpResponse(image)

def gpx(request, id):
    context = {
        "id": id
    }
    return render(request, "dashboard/gpx.html", context)

def map(request):
    context = {
        "mapboxAccessToken": mapboxAccessToken,
        "user": request.user,
        "location": getGPSLocation(),
    }
    return render(request, "dashboard/map.html", context)

@gzip.gzip_page
def cameraStream(request, id):
    try:
        return StreamingHttpResponse(cameras[id].frame_gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print("CANT START CAMERA '{}'".format(id))
        return HttpResponse("Ei voittoa")

def multiCameraView(request):
    availableCameras = Camera.objects.all()
    if not availableCameras:
        availableCameras = []

    context = {
        "user": request.user,
        "location": getGPSLocation(),
        "cameras": availableCameras
    }
    return render(request, "dashboard/cameras.html", context)

def cameraSettings(request, id):
    camera = Camera.objects.get(device_id=id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CameraForm(request.POST)
        if form.is_valid():
            print("CLEAN FORM DATA:", form.cleaned_data)
            return HttpResponseRedirect("/settings/camera/" + id + "/")
    else:
        initial_fields = model_to_dict(camera)
        form = CameraForm(initial=initial_fields)

    context = {
        "form": form
    }
    return render(request, "dashboard/camera-settings.html", context)
