from django.db import models


class StatusPartida(models.TextChoices):
    AGENDADA = "AG", "Agendada"
    EM_ANDAMENTO = "EA", "Em andamento"
    FINALIZADA = "FI", "Finalizada"


class ResultadoPartida(models.TextChoices):
    VITORIA = "V", "Vitória"
    DERROTA = "D", "Derrota"
    EMPATE = "E", "Empate"