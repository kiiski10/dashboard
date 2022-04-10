from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Profile, Location, Camera
from .forms import ProfileForm, LocationForm, CameraForm, SelectProfileForm
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


def editProfile(request):
	profileId = request.session.get("selectedProfile", None)
	profile = Profile.objects.get(pk=profileId)
	if request.method == 'POST':
		form = ProfileForm(
			request.POST,
			request.FILES,
			instance=profile
		)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("profile"))
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


def unsetProfile(request):
	request.session["selectedProfile"] = None
	return(HttpResponseRedirect(reverse("index")))


def index(request):
	profileId = request.session.get("selectedProfile", None)

	if profileId:
		profile = get_object_or_404(Profile, pk=profileId)
	else:
		return(HttpResponseRedirect(reverse("selectProfile")))

	request.session["selectedProfile"] = profileId

	return render(
		request, 'dashboard/index.html', {
			"mapboxAccessToken": mapboxAccessToken,
			"location": getGPSLocation(),
			"profile": profile,
		}
	)


def externalMap(request, zoom, flat, flon, tlat, tlon):
	mapProvider = "https://openstreetmap.org/"
	mapURL = "{0}directions?from={4},{5}&to={2},{3}".format(
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
	profileId = request.session.get("selectedProfile", None)
	profile = Profile.objects.filter(pk=profileId).first()
	form = SelectProfileForm(initial={'profile': profileId})

	context = {
		"profile": profile,
		"form": form,
	}
	return render(request, "dashboard/select-profile.html", context)


def profile(request):

	if request.method == 'POST':
		profileId = request.POST["profile"]
		profile = get_object_or_404(Profile, pk=profileId)
		request.session["selectedProfile"] = profileId
	else:
		profileId = request.session.get("selectedProfile", None)
		profile = get_object_or_404(Profile, pk=profileId)

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
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)
	lat = request.GET.get("lat", None)
	lon = request.GET.get("lon", None)

	if not lat or not lon:
		location = getGPSLocation()
	else:
		location = {"lat": lat, "lon": lon}

	context = {
		"mapboxAccessToken": mapboxAccessToken,
		"user": request.user,
		"location": location,
		"profile": profile,
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
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)

	availableCameras = Camera.objects.all()
	if not availableCameras:
		availableCameras = []

	context = {
		"user": request.user,
		"cameras": availableCameras,
		"profile": profile,
	}
	return render(request, "dashboard/cameras.html", context)


def cameraSettingView(request, camera_id):
	camera = Camera.objects.get(pk=camera_id)
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)
	form = CameraForm(model_to_dict(camera))

	context = {
		"form": form,
		"camera": camera,
		"profile": profile,
	}
	return render(request, "dashboard/camera-settings.html", context)


def locationList(request):
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)
	locations = profile.location_set.order_by("-created_date")
	context = {
		"profile": profile,
		"locations": locations,
	}
	return render(request, "dashboard/location-list.html", context)


def addLocation(request, lat, lon):
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)
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

	getParams = "?lat={}&lon={}".format(lat, lon)
	return HttpResponseRedirect("/p/map/{}".format(getParams))


def editLocation(request, location_id):
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)
	location = Location.objects.get(pk=location_id)

	if request.method == 'POST':
		form = LocationForm(
			request.POST,
			request.FILES,
			instance=location
		)
		if form.is_valid():
			form.save()
			getParams = "?lat={}&lon={}".format(location.lat, location.lon)
			return HttpResponseRedirect("/p/map/{}".format(getParams))
	else:
		form = LocationForm(instance=location)

	context = {
		"profile": profile,
		"location": location,
		"form": form,
	}
	return render(request, "dashboard/edit-location.html", context)


def settingsMenuView(request, kwargs=None):
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)

	if request.method == 'POST':
		camera_id = request.POST["camera_id"]
		camera = profile.cameras.get(pk=camera_id)
		form = CameraForm(request.POST, instance=camera)
		form.save()

	context = {
		"profile": profile,
	}
	return render(request, "dashboard/settings-menu.html", context)


def deleteLocationView(request, location_id):
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)
	location = get_object_or_404(Location, pk=location_id)
	location.delete()
	context = {
		"profile": profile,
	}
	getParams = "?lat={}&lon={}".format(location.lat, location.lon)
	return HttpResponseRedirect("/p/map/{}".format(getParams))


def setAsMyLocation(request, lat, lon):
	profileId = request.session.get("selectedProfile", None)
	profile = get_object_or_404(Profile, pk=profileId)

	context = {
		"profile": profile,
		"location": { "lat": lat, "lon": lon },
		"mapboxAccessToken": mapboxAccessToken,
	}

	return render(request, "dashboard/map.html", context)
