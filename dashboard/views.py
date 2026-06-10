from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from tournaments.models import Torneio, TorneioParticipante

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
        form = ProfileForm(instance=profile, initial={'cidade': profile.cidade.nome, 'estado': profile.cidade.estado
})


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
        jogador=request.user
    ).select_related('torneio').all().order_by(
        '-data_inscricao'
    )
    
    paginator = Paginator(partidas, 8) 
    page_obj = paginator.get_page(page_number)

    context = {
        'active_sidebar': 'historico',
        'partidas': page_obj
    }
    return render(request, 'dashboard/tournaments/historico_dashboard.html', context)


@login_required
def meus_torneios_view(request):
    """View da página de Meus Torneios no Dashboard"""
    context = {
        'active_sidebar': 'torneios'
    }
    return render(request, 'dashboard/tournaments/meus_torneios.html', context)
