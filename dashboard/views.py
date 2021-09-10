from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Profile
from .forms import ProfileForm

def editProfile(request, id):
    print("ID::::", id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
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
