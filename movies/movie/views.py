from django.shortcuts import render
from django.http import HttpResponse 
from .models import Movie

# Create your views here.


def Home(request):
    #return render(request, 'index.html', {'name': 'Miguel Vasquez Bojanini'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__contains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'index.html', {'searchTerm':searchTerm, 'movies':movies})

def About(request):
    return render(request, 'details.html')