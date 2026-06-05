from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from users.models import Profile
from users.services.usersServices import ProfileService
from users.forms import RegisterForm, ProfileForm

from users.services.exceptions import AltoLikeError

def register_view(request):
    """View criacao de Usuario"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, '.', {
        'form': form
    })


@login_required
def edit_profile(request):
    """View de edicao do Profile"""

    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

    
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

    p = get_object_or_404(Profile, user__username=username)
    context = {
    'user': p
    }
    return render(request, 'users/profile.html', context)


