"""
URL configuration for bracketmaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views.index import home, profile_view, toggle_like_view
from .views.dashboard import dashboard, meus_torneios_view
from .views.explore_torneios import explore_torneios
from .views.explore_profile import explore_profile
from .views.torneios_view import torneios_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', include('users.urls')),
    path('perfil/<str:nickname>/like/', toggle_like_view, name='toggle_like'),
    path('perfil/<str:nickname>/', profile_view, name='profile_view'),
    path('explore_torneios/', explore_torneios , name='explore_torneios'),
    # path('explore_perfis/', explore_profile, name='explore_profile'),
    path('torneios_view/', torneios_view, name='torneio_view'),
    path('dashboard/torneios/', meus_torneios_view, name='meus_torneios')

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )