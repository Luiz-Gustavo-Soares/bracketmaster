from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def meus_torneios_view(request):
    """View da página de Meus Torneios no Dashboard"""
    context = {
        'active_sidebar': 'torneios' # Faz a sidebar brilhar no menu correto
    }
    return render(request, 'dashboard/tournaments/meus_torneios.html', context)