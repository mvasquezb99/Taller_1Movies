from django.shortcuts import render
from .movieRecomendations import generateMovie, generateDescription, generateImage
# Create your views here.

def recomendations(request):
    searchTerm = request.GET.get('search')
    if (searchTerm):
        resTitle = generateMovie(searchTerm)
        resDesc = generateDescription(resTitle)
        resImage = generateImage(resTitle)
        print(resImage)
    else:
        resTitle = ''
        resDesc = ''
        resImage = ''
    return render(request, 'recomendations.html', {'response':resTitle, 'description': resDesc, 'urlImage': resImage})