from django.db import models


class TipoTorneio(models.TextChoices):
    CASUAL = "CA", "Casual"
    COMPETITIVA = "CO", "Competitiva"

class FormatoJogo(models.TextChoices):
    STANDARD = "ST", "Standard"
    COMMANDER = "CM", "Commander"
    MODERN = "MO", "Modern"
    PIONEER = "PI", "Pioneer"
    DRAFT = "DR", "Draft"