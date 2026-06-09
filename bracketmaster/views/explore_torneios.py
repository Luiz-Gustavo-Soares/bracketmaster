from django.shortcuts import render
from datetime import date
from django.core.paginator import Paginator 
from .index import MockTorneio 

def explore_torneios(request):
    return render(request, 'explore_torneios.html')