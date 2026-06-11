from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.core.exceptions import PermissionDenied as PermissionDeniedDjango

from tournaments.models import Torneio, TorneioParticipante, Rodada
from tournaments.forms import TorneioForm
from tournaments.enums import StatusTorneio, FormatoJogo, StatusRodada, FormatoTorneio
from tournaments.services.registroService import TournamentRegistrationService
from tournaments.services.rankinService import RankingService
from tournaments.services.torneioService import TournamentService

from matches.services.partidada_service import PartidaService
from matches.models import Partida, ParticipacaoPartida
from matches.enums import StatusPartida

from matches.services.exceptions import MatchNotFinishedError, MultipleWinnersError
from tournaments.services.exceptions import RegistrationError
from core.exceptions import PermissionDenied
from core.models import Cidade

from users.models import Profile




def busc_torneios(request):

    # Estilo da busca ?nome=dinos&formato=commander&cidade=diamantina...

    nome = request.GET.get('nome', None)
    formato = request.GET.get('formato', None)
    cidade = request.GET.get('local', None)
    data_fim = request.GET.get('data', None)
    ocultar_finalizados = request.GET.get('ocultar_finalizados', 'true').lower() == 'true'
    page_number = request.GET.get('page', 1)

    torneios = Torneio.objects.select_related('cidade').all().order_by()
    
    destaque = torneios[0] if torneios else None

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

    if data_fim:
        data_fim = parse_date(data_fim)

        if data_fim:
            torneios = torneios.filter(
                data_inicio__date__lte=data_fim
            )

    torneios = torneios.order_by('data_inicio')

    torneios_paginator = Paginator(torneios, 10)
    torneios_page = torneios_paginator.get_page(page_number)

    recent_champions = Profile.objects.all().order_by(
        'user__likes_recebidos'
    )[:3]
 
    
    context = {
        'torneios': torneios_page,
        'featured_tournament': destaque,
        'total_torneios': torneios.count(),
        'recent_champions': recent_champions

    }

    return render(request, 'explore_torneios.html', context)



def torneio(request, id_torneio):
    torneio = get_object_or_404(
        Torneio,
        pk=id_torneio
    )

    rank = [p['participante'] for p in RankingService.calcular_ranking(torneio)]

    is_registered = torneio.participantes.filter(
        jogador=request.user
    ).exists()


    context = {
        'tournament': torneio,
        'standings': rank,
        'premiacoes': torneio.get_premiacoes_list(),
        'is_registered': is_registered
    }

    return render(request, 'torneio_view.html', context)


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
            
            endereco_list = [
                    form.cleaned_data('lagradouro'),
                    form.cleaned_data('numero'),
                    form.cleaned_data('bairro'),
                    form.cleaned_data('complemento'),
                ]

            endereco_list = [Cidade._normalizar(end) for end in endereco_list]
            
            torneio.local = ', '.join(endereco_list)
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

            endereco_list = [
                    form.cleaned_data('lagradouro'),
                    form.cleaned_data('numero'),
                    form.cleaned_data('bairro'),
                    form.cleaned_data('complemento'),
                ]

            endereco_list = [Cidade._normalizar(end) for end in endereco_list]
            
            torneio.local = ', '.join(endereco_list)
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


@login_required
def aprovar_participante(request, torneio_id, participante_id):
    """Aprova um participante em um torneio em especifico"""
    participante = get_object_or_404(
        TorneioParticipante,
        id=participante_id,
        torneio_id=torneio_id
    )

    try:
        TournamentRegistrationService.approvar_jogador(participante, request.user)
        messages.success(
            request,
            'Participante aprovado.'
        )
    except PermissionDenied as e:
        messages.error(
            request,
            'Permição negada, voce não é o ornanizador!'
        )

    except Exception as e:
        messages.error(
            request,
            'Erro desconhecido!'
        )

    return redirect('meus_torneios_participantes_edit', pk=torneio_id, edit='edit')


@login_required
def rejeitar_participante(request, torneio_id, participante_id):
    """Rejeita um participante em um torneio em especifico"""
    participante = get_object_or_404(
        TorneioParticipante,
        id=participante_id,
        torneio_id=torneio_id
    )

    try:
        TournamentRegistrationService.regeitar_jogador(participante, request.user)
        messages.success(
            request,
            'Participante rejeitado.'
        )
    except PermissionDenied as e:
        messages.error(
            request,
            'Permição negada, voce não é o ornanizador!'
        )

    except Exception as e:
        messages.error(
            request,
            'Erro desconhecido!'
        )

    return redirect('meus_torneios_participantes_edit', pk=torneio_id, edit='edit')


@login_required
@require_POST
def inscrever_torneio(request, torneio_id):
    """Inscreve um participante em um torneio em especifico"""
    torneio = get_object_or_404(
        Torneio,
        id=torneio_id
    )

    try:
        TournamentRegistrationService.adicionar_jogador(torneio, request.user)
        messages.success(
            request,
            'Participante inscrito.'
        )
    except RegistrationError as e:
        messages.error(
            request,
            str(e)
        )

    except Exception as e:
        messages.error(
            request,
            'Erro desconhecido!'
        )

    return redirect('torneio_view', id_torneio=torneio_id)



@login_required
@require_POST
def alter_status_torneio(request, torneio_id, new_status):
    torneio = get_object_or_404(
        Torneio,
        id=torneio_id
    )

    if torneio.organizador != request.user:
        raise PermissionDeniedDjango()

    actions = {
        'abrir_inscricoes': TournamentService.abrir_inscricoes,
        'encerrar_inscricoes': TournamentService.encerrar_inscricoes,
        'iniciar': TournamentService.iniciar,
        'proxima_rodada': TournamentService.proxima_rodada,
    }

    action = actions.get(new_status)

    if action is None:
        raise Http404()

    try:
        action(torneio)
        messages.success(request, 'Status alterado com sucesso.')

    except Exception as e:
        messages.error(request, 'Erro ao alterar status')

    return redirect('play', torneio_id=torneio_id)


@login_required
@require_POST
def resetar_torneio(request, torneio_id):
    torneio = get_object_or_404(
        Torneio,
        id=torneio_id
    )

    if torneio.organizador != request.user:
        raise PermissionDeniedDjango()
    
    
    try:
        TournamentService.resetar_torneio(torneio, request.user)
        messages.success(request, 'Board Wipe nao foi anulado')

    except Exception as e:
        messages.error(request, 'Anularam...')

    return redirect('play', torneio_id=torneio_id)


@login_required
@require_POST
def definir_ganhador_partida(request, torneio_id):
    
    match_id = request.POST.get('match_id')
    result = request.POST.get('winner_id')

    partida = get_object_or_404(Partida, pk=match_id, rodada__torneio__organizador=request.user)
    
    par_partida = None
    if result:
        par_partida = ParticipacaoPartida.objects.filter(pk=result).first()

    if partida.rodada.status != StatusRodada.FINALIZADA:
        PartidaService.registrar_resultado(partida, par_partida)
        PartidaService.finalizar_partida(partida)
    return redirect('play', torneio_id=torneio_id)


def play_view(request, torneio_id):
    torneio = get_object_or_404(
        Torneio,
        id=torneio_id
    )


    rodada_atual = int(request.GET.get('rodada', 0))
    
    num_rodadas = torneio.rodadas.count()

    rodada_atual = rodada_atual if rodada_atual else num_rodadas
    
    num_rodadas_finalizadas = torneio.rodadas.filter(status=StatusRodada.FINALIZADA).count()
    progresso_torneio = round(num_rodadas_finalizadas / torneio.numero_rodadas * 100)
    
    classificacao = RankingService.calcular_ranking(torneio, elim=torneio.formato_torneio == FormatoTorneio.SINGLE_ELIM)
    
    rodada = Rodada.objects.filter(torneio=torneio, numero=rodada_atual).first()


    matches = []
    is_round_finished = False
    completed_matches = 0
    total_matches = 0

    if rodada:
        is_round_finished = rodada.is_finished()
        partidas = rodada.partidas.all()

        total_matches = partidas.count()
        completed_matches = partidas.filter(status=StatusPartida.FINALIZADA).count()

        for partida in partidas:
            participantes = list(partida.participacoes.all())
            
            p1 = participantes.pop()
            
            if participantes: 
                p2 = participantes.pop()
            else:
                p2 = None
            winner = None

            try:
                winner = PartidaService.ganhador(partida)
                winner = winner if winner else 'draw'
                
            except MatchNotFinishedError as e:
                pass
            
            except MultipleWinnersError as e:
                pass

            matches.append({
                'partida': partida,
                'winner': winner,
                'player1': p1,
                'player2': p2,
            })

    context = {
        'tournament': torneio,
        'current_round': rodada_atual,
        'progresso_torneio': progresso_torneio,
        'standings': classificacao,
        'total_rounds_range': range(1, num_rodadas+1),
        'matches': matches,
        'is_round_finished': is_round_finished,
        'completed_matches': completed_matches,
        'total_matches': total_matches,
        'view_organizador': torneio.organizador == request.user,
        'pending_matches': total_matches-completed_matches
    }

    return render(request, 'dashboard/tournaments/play.html', context=context)