from django.shortcuts import render, get_object_or_404, redirect


def play_view(request):
    return render(request, 'dashboard/tournaments/play.html')