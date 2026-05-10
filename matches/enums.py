from django.db import models


class StatusPartida(models.TextChoices):
    AGENDADA = "AG", "Agendada"
    EM_ANDAMENTO = "EA", "Em andamento"
    FINALIZADA = "FI", "Finalizada"
    CANCELADA = "CA", "Cancelada"

class TipoPartida(models.TextChoices):
    CASUAL = "CA", "Casual"
    COMPETITIVA = "CO", "Competitiva"

class FormatoJogo(models.TextChoices):
    STANDARD = "ST", "Standard"
    COMMANDER = "CM", "Commander"
    MODERN = "MO", "Modern"
    PIONEER = "PI", "Pioneer"
    DRAFT = "DR", "Draft"

class ResultadoPartida(models.TextChoices):
    VITORIA = "V", "Vitória"
    DERROTA = "D", "Derrota"
    EMPATE = "E", "Empate"