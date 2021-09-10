from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('p/<str:id>/', views.profile, name='profile'),
    path('ep/<str:id>/', views.editProfile, name='editProfile'),
    path('media/img/<str:name>/', views.image, name='image'),
    path('media/g/<str:id>/', views.gpx, name='gpx'),
]
