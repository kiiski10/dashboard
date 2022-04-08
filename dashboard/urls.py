from django.urls import path, include
from . import views

profile_patterns = [
    path("", views.profile, name="profile"),
    path("e/", views.editProfile, name="editProfile"),
    path("map/", views.map, name="map"),
    path("locations/", views.locationList, name="locationList"),
    path("unset/", views.unsetProfile, name="unsetProfile"),
    path("edit-location/<int:location_id>", views.editLocation, name="editLocation"),
    path("add-location/<str:lat>/<str:lon>/", views.addLocation, name="addLocation"),
    path("cameras/", views.multiCameraView, name="multiCameraView"),
    path("camera/<int:id>/", views.cameraStream, name="cameraStream"),
    path("settings/camera/<int:camera_id>/", views.cameraSettings, name="cameraSettingView"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("p/", include(profile_patterns)),
    path("sp/", views.selectProfile, name="selectProfile"),
    path("media/img/<str:name>", views.image, name="image"),
    path("media/g/<str:id>/", views.gpx, name="gpx"),
    path("external-map/<str:zoom>/<str:flat>/<str:flon>/<str:tlat>/<str:tlon>/", views.externalMap, name="externalMap"),
]
