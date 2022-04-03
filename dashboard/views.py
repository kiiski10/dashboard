from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Profile, Location, Camera
from .forms import ProfileForm, LocationForm, CameraForm
from django.views.decorators import gzip
from django.http import StreamingHttpResponse # for LiveView
from django.forms.models import model_to_dict
from django.urls import reverse

import cv2
from .utilities import camera
import random
import reverse_geocoder

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

def editProfile(request, profile_id):
	profile = Profile.objects.get(pk=profile_id)
	if request.method == 'POST':
		form = ProfileForm(
			request.POST,
			request.FILES,
			instance=profile
		)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("profile", args=[profile_id]))
	else:
		form = ProfileForm(model_to_dict(profile))

	return render(request, 'dashboard/edit-profile.html', {
			"mapboxAccessToken": mapboxAccessToken,
			"location": getGPSLocation(),
			"id": id,
			"form": form,
			"profile": profile,
		}
	)

def index(request):
	return HttpResponseRedirect("/sp/")

def externalMap(request, zoom, flat, flon, tlat, tlon):
	mapProvider = "https://openstreetmap.org/"
	mapURL = "{0}directions?from={2},{3}&to=#map={1}/{4}/{5}".format(
		mapProvider,
		zoom,
		flat,
		flon,
		tlat,
		tlon,
	)
	return HttpResponseRedirect(mapURL)

def selectProfile(request):
	profiles = Profile.objects.all()
	context = {
		"profiles": profiles,
		"location": getGPSLocation()
	}
	return render(request, "dashboard/select-profile.html", context)

def profile(request, profile_id):
	profile = Profile.objects.get(pk=profile_id)
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

def map(request, profile_id):
	profile = Profile.objects.get(pk=profile_id)
	context = {
		"mapboxAccessToken": mapboxAccessToken,
		"user": request.user,
		"location": getGPSLocation(),
		"profile": profile,
	}
	return render(request, "dashboard/map.html", context)

@gzip.gzip_page
def cameraStream(request, id, profile_id):
	try:
		return StreamingHttpResponse(cameras[id].frame_gen(), content_type="multipart/x-mixed-replace;boundary=frame")
	except Exception as e:
		print("CANT START CAMERA '{}'".format(id))
		return HttpResponse("Ei voittoa")

def multiCameraView(request, profile_id):
	profile = Profile.objects.get(pk=profile_id)
	availableCameras = Camera.objects.all()
	if not availableCameras:
		availableCameras = []

	context = {
		"user": request.user,
		"location": getGPSLocation(),
		"cameras": availableCameras,
		"profile": profile,
	}
	return render(request, "dashboard/cameras.html", context)

def cameraSettings(request, profile_id, camera_id):
	camera = Camera.objects.get(pk=camera_id)
	profile = Profile.objects.get(pk=profile_id)

	if request.method == 'POST':
		form = CameraForm(request.POST, instance=camera)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("multiCameraView", args=[profile_id]))
	else:
		form = CameraForm(model_to_dict(camera))

	context = {
		"id": camera_id,
		"form": form,
		"camera": camera,
		"profile": profile,
	}
	return render(request, "dashboard/camera-settings.html", context)

def locationList(request, profile_id):
	profile = Profile.objects.get(pk=profile_id)
	context = {
		"profile": profile,
	}
	return render(request, "dashboard/location-list.html", context)

def addLocation(request, profile_id, lat, lon):
	profile = Profile.objects.get(pk=profile_id)
	coordinates = [lat, lon]
	geocode_results = reverse_geocoder.search(coordinates)
	place_name = "{}, {}, {}".format(geocode_results[0]["name"], geocode_results[0]["admin1"], geocode_results[0]["cc"])

	location = Location.objects.create(
		creator=profile,
		label=place_name,
		note="{}, {}".format(lat[:4], lon[:4]),
		location_type="WAYPOINT",
		lat=lat,
		lon=lon,
	)
	return HttpResponseRedirect(reverse("map", args=[profile_id]))

def editLocation(request, profile_id, location_id):
	profile = Profile.objects.get(pk=profile_id)
	location = Location.objects.get(pk=location_id)

	if request.method == 'POST':
		form = LocationForm(request.POST, instance=location)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("locationList", args=[profile_id]))
	else:
		form = LocationForm(instance=location)

	context = {
		"profile": profile,
		"location": location,
		"form": form,
	}
	return render(request, "dashboard/edit-location.html", context)