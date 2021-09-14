from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Profile
from .forms import ProfileForm
from django.views.decorators import gzip
from django.http import StreamingHttpResponse # for LiveView
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
cam = camera.Camera(0)
print(cam.video.isOpened())

def getGPSLocation():
    # import gpsd
    # gpsd.connect()
    # packet = gpsd.get_current()
    # print(packet.position())
    #
    # fake it till u make it
    lat = str(61.289 + random.randint(-5,5))
    lon = str(28.840 + random.randint(-5,5))
    print("GOT LOCATION:", lat, lon)
    return({"lat": lat.ljust(8, "0"), "lon": lon.ljust(8, "0")})

currentLocation = getGPSLocation()

def editProfile(request, id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("CLEAN FORM DATA:", form.cleaned_data)
            return HttpResponseRedirect("/ep/" + id + "/")

    else:
        # TODO: prepopulate fields
        form = ProfileForm()

    return render(request, 'dashboard/edit-profile.html', {
            "id": id,
            "form": form
        }
    )

def index(request):
    currentLocation = getGPSLocation()
    return HttpResponseRedirect("/sp/")

def map(request):
    zoom = 10
    mapProvider = "https://openstreetmap.org/"
    mapURL = "{0}directions?from={2},{3}&to=#map={1}/{2}/{3}".format(
        mapProvider,
        zoom,
        currentLocation["lat"],
        currentLocation["lon"],
    )
    print("URL::", mapURL)
    return HttpResponseRedirect(mapURL)

def selectProfile(request):
    profiles = Profile.objects.all()
    context = { "profiles": profiles, "location": currentLocation }
    return render(request, "dashboard/select-profile.html", context)

def profile(request, id):
    profile = Profile.objects.get(pk=id)
    context = { "profile": profile, "location": currentLocation }
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

@gzip.gzip_page
def cameraView(request, id):
    try:
        return StreamingHttpResponse(cam.frame_gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print("CAMERA ERROR:", e)
        return HttpResponse("Ei voittoa")
