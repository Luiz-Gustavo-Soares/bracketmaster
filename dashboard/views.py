from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from core.models import Cidade

from tournaments.models import Torneio, TorneioParticipante
from tournaments.forms import TorneioForm
from tournaments.enums import StatusInscricao, StatusTorneio

from users.models import Profile
from users.forms import ProfileForm


@login_required
def dashboard(request):
    """View de edicao do Profile"""

    profile = Profile.objects.com_taxa_vitoria().get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            instance=profile
        )
        
        if form.is_valid():
            profile: Profile = form.save(commit=False)
            profile.adicionar_cidade(form.cleaned_data['cidade'], form.cleaned_data['estado'])
            profile.save()

    
    else: 
        if profile.cidade:
            form = ProfileForm(instance=profile, initial={'cidade': profile.cidade.nome, 'estado': profile.cidade.estado})
        else:
            form = ProfileForm(instance=profile)



    context = {
        'active_sidebar': 'perfil',
        'form':form,
        'profile': profile
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def historico_dashboard_view(request):
    page_number = request.GET.get('page', None)

    partidas = TorneioParticipante.objects.filter(
        jogador=request.user,
        torneio__status=StatusTorneio.FINALIZADO
    ).select_related('torneio').all().order_by(
        '-data_inscricao',
    )
    
    paginator = Paginator(partidas, 8) 
    page_obj = paginator.get_page(page_number)

    context = {
        'active_sidebar': 'historico',
        'partidas': page_obj
    }
    return render(request, 'dashboard/tournaments/historico_dashboard.html', context)


@login_required
def meus_torneios_view(request, pk=None, edit=False):
    """View da página de Meus Torneios no Dashboard"""

    torneio_participantes_edit = None
    torneio_edicao = None
    torneio_participantes_edit_list = None
    
    if pk:
        torneio_edicao = get_object_or_404(
            Torneio,
            pk=pk,
            organizador=request.user
        )

        if edit == 'edit':
            torneio_participantes_edit = True   
            torneio_participantes_edit_list = TorneioParticipante.objects.filter(
                torneio = torneio_edicao,
                ).select_related('torneio').all()
            
            torneio_participantes_edit_list = torneio_participantes_edit_list.order_by('status')


    inscricoes = TorneioParticipante.objects.filter(
        jogador=request.user,
    ).select_related('torneio').all()
    inscricoes = inscricoes.exclude(torneio__status=StatusTorneio.FINALIZADO)

    torneios_criados = Torneio.objects.filter(organizador=request.user).all().order_by('status')

    if request.method == "POST":
        form = TorneioForm(
            request.POST,
            instance=torneio_edicao
        )

        if form.is_valid():
            torneio = form.save(commit=False)

            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']

            endereco_list = [
                    form.cleaned_data['lagradouro'],
                    form.cleaned_data['numero'],
                    form.cleaned_data['bairro'],
                    form.cleaned_data['complemento'],
                ]

            endereco_list = [Cidade._normalizar(end) for end in endereco_list]
            
            torneio.local = ', '.join(endereco_list)
            torneio.adicionar_cidade(cidade, estado)

            if not torneio_edicao:
                torneio.organizador = request.user

            torneio.save()
            return redirect("meus_torneios")

    else:
        if torneio_edicao:
            ini = {'cidade': torneio_edicao.cidade.nome, 'estado': torneio_edicao.cidade.estado, 'lagradouro': torneio_edicao.local}
            form = TorneioForm(instance=torneio_edicao, initial=ini)
        else:
            form = TorneioForm()
    
    context = {
        'active_sidebar': 'torneios',
        'inscricoes': inscricoes,
        'torneios_criados': torneios_criados,
        'form': form,
        'torneio_edicao': torneio_edicao,
        'torneio_participantes_edit': torneio_participantes_edit,
        'torneio_participantes_edit_list': torneio_participantes_edit_list,
    }

    return render(request, 'dashboard/tournaments/meus_torneios.html', context)
