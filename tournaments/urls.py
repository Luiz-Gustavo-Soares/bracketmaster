from django.urls import path
from tournaments.views import busc_torneios, torneio


urlpatterns = [
    path('buscar/', busc_torneios, name='buscar_torneios'),
    path('<int:torneio>', torneio, name='torneio'),
]
