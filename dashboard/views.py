from django.http import HttpResponse
from django.template import loader
from .models import Car

def index(request):
    cars = Car.objects.order_by('-name')[:5]
    template = loader.get_template('dashboard/index.html')
    context = {
        'cars': cars,
    }
    return HttpResponse(template.render(context, request))
