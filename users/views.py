from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import RegisterForm, ProfileForm, LoginForm
from django.contrib.auth.models import User


def register_view(request):
    """View criacao de Usuario"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["password"]
            username = form.cleaned_data["username"]
            
            user = User.objects.create(username=username, email=email, password=senha)

            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {
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
    return render(request, 'users/profile.html', context)


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

