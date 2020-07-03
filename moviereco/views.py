from django.shortcuts import render

import json
from django.views import View
from django.http import HttpResponse

from .recommendation_system import *

def RecommendMovie(request, word):
    result = recommendMovies(int(word), 10)
    return HttpResponse(result)
