from django.urls import path
from tournaments.views import busc_torneios, torneio, aprovar_participante, rejeitar_participante, play_view, alter_status_torneio


urlpatterns = [
    path('explore_torneios/', busc_torneios , name='explore_torneios'),
    path('torneio/participantes/aprovar/<int:torneio_id>/<int:participante_id>', aprovar_participante, name='aprovar_participante'),
    path('torneio/participantes/rejeitar/<int:torneio_id>/<int:participante_id>', rejeitar_participante, name='rejeitar_participante'),
    path('play/<int:torneio_id>', play_view, name='play'),
    path('play/<int:torneio_id>/alter-status/<str:new_status>', alter_status_torneio, name='play-alt-status'),
    path('torneio/<int:id_torneio>', torneio, name='torneio_view'),
]
