from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from tournaments.models import Torneio
from tournaments.enums import StatusTorneio, FormatoJogo
from django.utils.dateparse import parse_date

def busc_torneios(request):

    # Estilo da busca ?nome=dinos&formato=commander&cidade=diamantina...

    nome = request.GET.get('nome', None)
    formato = request.GET.get('formato', None)
    cidade = request.GET.get('cidade', None)
    data_fim = request.GET.get('data', None)
    ocultar_finalizados = request.GET.get('ocultar_finalizados', 'true').lower() == 'true'
    page_number = request.GET.get('page', 1)

    torneios = Torneio.objects.select_related('cidade').all()

    if ocultar_finalizados:
        torneios = torneios.exclude(
            status=StatusTorneio.FINALIZADO
        )

        torneios = torneios.filter(
            data_inicio__gte = timezone.now()
        )

    if nome:
        torneios = torneios.filter(
            nome__icontains=nome
        )

    if formato in dict(FormatoJogo.choices):
        torneios = torneios.filter(
            formato_torneio=formato
        )

    if cidade:
        torneios = torneios.filter(
            cidade__nome__icontains=cidade
        )

    data_fim = parse_date(data_fim)

    if data_fim:
        torneios = torneios.filter(
            data_inicio__date__lte=data_fim
        )

    torneios = torneios.order_by('data_inicio')

    torneios_paginator = Paginator(torneios, 10)
    torneios_page = torneios_paginator.get_page(page_number)


    
    context = {
        'torneios': torneios_page,
        'destaque': torneios.first() # tem q ver isso ainda
    }

    return render(request, 'torneios.html', context)
