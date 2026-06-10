from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile
from .forms import RegisterForm, ProfileForm


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

    return render(request, 'users/registration/register.html', {
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


def profile(request, username):
    """View de renderizacao de um usuario em questao
    Args:
        username (str): username referente a um User
    """

    p = get_object_or_404(Profile, user__username=username)
    context = {
    'profile': p
    }
    return render(request, 'users/profile_view.html', context)
