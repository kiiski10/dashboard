from django.urls import path, include
from . import views

profile_patterns = [
    path("<str:profile_id>/", views.profile, name="profile"),
    path("<str:profile_id>/e/", views.editProfile, name="editProfile"),
    path("<str:profile_id>/map/", views.map, name="map"),
    path("<str:profile_id>/locations/", views.locationList, name="locationList"),
    path("<str:profile_id>/cameras/", views.multiCameraView, name="multiCameraView"),
    path("<str:profile_id>/camera/<int:id>/", views.cameraStream, name="cameraStream"),
    path("<str:profile_id>/settings/camera/<int:camera_id>/", views.cameraSettings, name="cameraSettingView"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("p/", include(profile_patterns)),
    path("sp/", views.selectProfile, name="selectProfile"),
    path("media/img/<str:name>", views.image, name="image"),
    path("media/g/<str:id>/", views.gpx, name="gpx"),
    path("external-map/<str:zoom>/<str:lat>/<str:lon>/", views.externalMap, name="externalMap"),
]
