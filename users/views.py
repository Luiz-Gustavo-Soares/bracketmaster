from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from users.models import Profile, ProfileLike
from users.services.usersServices import ProfileService
from users.forms import RegisterForm, ProfileForm, LoginForm
from users.services.exceptions import AltoLikeError
from tournaments.models import TorneioParticipante


def register_view(request):
    """View criacao de Usuario"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["password"]
            username = form.cleaned_data["username"]
            
            if not User.objects.filter(email=email).exists():

                user = User.objects.create(username=username, email=email, password=senha)

                login(request, user)
                return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def edit_profile(request):
    """View de edicao do Profile"""

    profile = request.user.profile
    
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
        form = ProfileForm(instance=profile)

    context = {
        'form':form
    }
    
    return render(request, 'users/edit_profile.html', context)


@login_required
def like_profile(request, username):

    perfil = get_object_or_404(
        User,
        username=username
    )

    try:

        liked = ProfileService.toggle_like(
            request.user,
            perfil
        )

        return JsonResponse({
            "liked": liked
        })

    except AltoLikeError as e:

        return JsonResponse({
            "error": str(e)
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            "error": 'Erro Interno'
        }, status=500)
    

def profile(request, username):
    """View de renderizacao de um usuario em questao
    Args:
        username (str): username referente a um User
    """

    try:
        p = Profile.objects.com_taxa_vitoria().get(
            user__username=username
        )

    except Profile.DoesNotExist:
        raise Http404("Article not found.")
    
    page_number = request.GET.get('page', 1)

    participacoes = TorneioParticipante.objects.aprovados().filter(
        jogador=p.user
        ).order_by(
            '-data_inscricao'
        )
    
    

    torneios_paginator = Paginator(participacoes, 5)
    torneios_page = torneios_paginator.get_page(page_number)
    is_liked = p.user.likes_recebidos.filter(usuario_que_curtiu=request.user).exists()
    context = {
        'profile': p,
        'taxa_vitoria': p.taxa_vitoria,
        'historico': torneios_page,
        'is_liked': is_liked
    }
    
    return render(request, 'users/profile_view.html', context)


def login_view(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["password"]

            username = User.objects.filter(email=email).first().username

            user = authenticate(request, username=username, password=senha)
            if user is not None:
                login(request, user)

                return redirect('home')

    return render(
        request, "users/login.html", {"form": form}
    )


def busc_profile(request):
    nome = request.GET.get('nome', None)
    cidade = request.GET.get('cidade', None)
    page = request.GET.get('page', 1)


    perfis = Profile.objects.com_taxa_vitoria().select_related('cidade').all().order_by('user__likes_recebidos')
    top_profiles = perfis[:3]

    if nome:
        perfis = perfis.filter(
            nickname__icontains=nome
        )

    perfis_paginator = Paginator(perfis, 20)
    perfis_page = perfis_paginator.get_page(page)
    
    context = {
        'perfis': perfis_page,
        'top_profiles': top_profiles,
    }

    return render(
        request, 'explore_profile.html', context
    )