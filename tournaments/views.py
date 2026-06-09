from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.dateparse import parse_date
from tournaments.models import Torneio
from tournaments.forms import TorneioForm
from tournaments.enums import StatusTorneio, FormatoJogo
from core.models import Cidade


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



def torneio(request, id_torneio):
    torneio = get_object_or_404(
        Torneio,
        pk=id_torneio
    )

    context = {
        'torneio': torneio
    }
    return render(request, 'torneio.html', context)


@login_required
def edit_torneio(request, id_torneio):
    torneio = get_object_or_404(
        Torneio,
        pk=id_torneio,
        organizador=request.user
    )

    if request.method == 'POST':
        form = TorneioForm(request.POST, instance=torneio)
        if form.is_valid():
            torneio: Torneio = form.save(commit=False)
            cidade = form.cleaned_data('cidade')
            estado = form.cleaned_data('estado')

            torneio.adicionar_cidade(cidade, estado)
            
            return redirect('dash')
    else:
        form = TorneioForm(instance=torneio)

    context = {
        'form': form
    }
    return render(request, 'torneio-edit.html', context)


@login_required
def criar_torneio(request):
    if request.method == 'POST':
        form = TorneioForm(request.POST)
        if form.is_valid():
            torneio: Torneio = form.save(commit=False)
            cidade = form.cleaned_data('cidade')
            estado = form.cleaned_data('estado')

            torneio.adicionar_cidade(cidade, estado)
            torneio.organizador = request.user

            torneio.save()
            return redirect('dash')
    else:
        form = TorneioForm()

    context = {
        'form': form
    }
    return render(request, 'torneio-edit.html', context)
