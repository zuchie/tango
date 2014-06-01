from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hello yo! <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse("This is about page. <a href='/rango/index'>Index</a>")

