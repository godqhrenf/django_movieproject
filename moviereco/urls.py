from django.urls 	import path
from .views	import RecommendMovie

urlpatterns = [
  path('moviereco/<word>/', RecommendMovie)
]