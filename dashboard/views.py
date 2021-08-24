from django.http import HttpResponse


def index(request):
    return HttpResponse("""Hello, human. Im your car""")