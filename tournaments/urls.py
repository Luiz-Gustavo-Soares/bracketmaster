from django.urls import path
from tournaments.views import busc_torneios, torneio


urlpatterns = [
    path('explore_torneios/', busc_torneios , name='explore_torneios'),
    path('<int:torneio>', torneio, name='torneio'),
]
