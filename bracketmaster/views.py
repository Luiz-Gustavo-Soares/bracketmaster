from django.shortcuts import render, get_object_or_404, redirect



def home(request):
    """Pagina inicial da aplicação"""
    user = request.user
    return render(request, 'index.html')
