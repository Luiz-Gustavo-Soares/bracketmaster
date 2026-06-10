from django.urls import path
from dashboard.views import dashboard, historico_dashboard_view, meus_torneios_view

urlpatterns = [
    path('', dashboard , name='dashboard'),
    path('historico/', historico_dashboard_view, name='historico_dashboard'),
    path('torneios/', meus_torneios_view, name='meus_torneios'),
    path('torneios/<int:pk>', meus_torneios_view, name='meus_torneios_edit'),
    path('torneios/<int:pk>/<str:edit>', meus_torneios_view, name='meus_torneios_participantes_edit'),
]
