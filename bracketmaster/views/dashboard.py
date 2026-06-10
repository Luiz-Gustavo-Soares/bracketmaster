from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def meus_torneios_view(request):
    """View da página de Meus Torneios no Dashboard"""
    context = {
        'active_sidebar': 'torneios' # Faz a sidebar brilhar no menu correto
    }
    return render(request, 'dashboard/tournaments/meus_torneios.html', context)

@login_required
def inbox_view(request):
    context = {
        'active_sidebar': 'inbox',
        'titulo_pagina': 'Inbox'
    }
    return render(request, 'dashboard/em_construcao.html', context)

@login_required
def decks_view(request):
    context = {
        'active_sidebar': 'decks',
        'titulo_pagina': 'Meus Decks'
    }
    return render(request, 'dashboard/em_construcao.html', context)

@login_required
def historico_dashboard_view(request):
    # Simulando os dados que virão do seu banco:
    partidas_mock = [
        {'torneio': 'Mix Diamantina', 'data': '14/06/26', 'formato': 'Commander', 'colocacao': '1º Lugar', 'status': 'win'},
        {'torneio': 'A Última Evolução', 'data': '29/05/26', 'formato': 'Draft', 'colocacao': 'Top 8', 'status': 'neutral'},
        {'torneio': 'Torneio Local Magic', 'data': '10/05/26', 'formato': 'Modern', 'colocacao': 'Eliminado', 'status': 'loss'},
        # Adicione mais itens aqui para testar a paginação visualmente
    ] * 5 # Multipliquei por 5 só para gerar volume de dados e a paginação aparecer
    
    # Configurando a paginação (ex: 8 partidas por página)
    paginator = Paginator(partidas_mock, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'active_sidebar': 'historico',
        'partidas': page_obj, # Passamos o page_obj para o template
    }
    return render(request, 'dashboard/tournaments/historico_dashboard.html', context)