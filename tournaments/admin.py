from django.contrib import admin
from tournaments.models import Torneio, TorneioParticipante

# Register your models here.
admin.site.register(Torneio)

admin.site.register(TorneioParticipante)