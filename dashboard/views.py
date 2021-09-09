from django.shortcuts import render
from .models import Car

def index(request):
    cars = Car.objects.all()
    context = { "cars": cars }
    return render(request, "dashboard/index.html", context)

def car(request, id):
    car = Car.objects.get(pk=id)
    context = { "car": car }
    return render(request, "dashboard/car.html", context)
