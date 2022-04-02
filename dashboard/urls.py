from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("p/<str:id>/", views.profile, name="profile"),
    path("ep/<str:id>/", views.editProfile, name="editProfile"),
    path("sp/", views.selectProfile, name="selectProfile"),
    path("map/", views.map, name="map"),
    path("media/img/<str:name>", views.image, name="image"),
    path("media/g/<str:id>/", views.gpx, name="gpx"),
    path("cameras/", views.multiCameraView, name="multiCameraView"),
    path("camera/<int:id>/", views.cameraStream, name="cameraView"),
    path("settings/camera/<int:id>/", views.cameraSettings, name="cameraSettingView"),
    path("external-map/<str:loc>", views.externalMap, name="externalMap"),
]
