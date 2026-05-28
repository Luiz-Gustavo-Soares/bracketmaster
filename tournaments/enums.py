from django.db import models


class TipoTorneio(models.TextChoices):
    CASUAL = "CA", "Casual"
    COMPETITIVO = "CO", "Competitivo"

class FormatoJogo(models.TextChoices):
    STANDARD = "ST", "Standard"
    COMMANDER = "CM", "Commander"
    MODERN = "MO", "Modern"
    PIONEER = "PI", "Pioneer"
    DRAFT = "DR", "Draft"


class StatusTorneio(models.TextChoices):
    CRIADO = 'CRIADO'
    INSCRICOES = 'INSCRICOES'
    INSCRICOES_E = 'INSCRICOES_ENCERRADAS'
    EM_ANDAMENTO = 'EM_ANDAMENTO'
    FINALIZADO = 'FINALIZADO'


class FormatoTorneio(models.TextChoices):
    SWISS = 'SWISS', 'Sistema Suiço'
    SINGLE_ELIM = 'SINGLE_ELIM', 'Eliminação Simples'


class StatusRodada(models.TextChoices):
    ABERTA = 'AB', 'Aberta'
    FINALIZADA = 'FI', 'Finalizada'
    