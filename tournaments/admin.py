from django.contrib import admin
from tournaments.models import Torneio, TorneioParticipante, Rodada

# Register your models here.
admin.site.register(Torneio)

admin.site.register(TorneioParticipante)
admin.site.register(Rodada)