from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Profile
from .forms import ProfileForm
from django.views.decorators import gzip
from django.http import StreamingHttpResponse # for LiveView
import cv2

def editProfile(request, id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            print("CLEAN FORM DATA:", form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect("/ep/" + id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm()

    return render(request, 'dashboard/editProfile.html', {
            "id": id,
            "form": form
        }
    )

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


from .utilities import camera

@gzip.gzip_page
def cameraView(request, id):
    cam = camera.Camera(0)
    try:
        return StreamingHttpResponse(cam.frame_gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print("CAMERA ERROR:", e)
        return HttpResponse("Ei voittoa")
