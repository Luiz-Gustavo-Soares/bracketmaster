from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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
        'form':form,
        'profile': profile
    }
    
    return render(request, 'dashboard/dashboard.html', context)