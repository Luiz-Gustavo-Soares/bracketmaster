from django.shortcuts import render, get_object_or_404, redirect


def explore_profile(request):
    return render(request, 'explore_profile.html')