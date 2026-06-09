from django.shortcuts import render, get_object_or_404, redirect


def torneios_view(request):
    return render(request, 'torneio_view.html')