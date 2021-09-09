from django.shortcuts import render
from .models import Car

def index(request):
    cars = Car.objects.all()
    context = { "cars": cars }
    return render(request, "dashboard/index.html", context)
