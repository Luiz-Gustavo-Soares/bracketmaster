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


class Fundos(models.TextChoices):
    Fundo1='monumento_magic', 'Monumento'


class StatusTorneio(models.TextChoices):
    CRIADO = 'CRIADO', 'Criado'
    INSCRICOES = 'ABERTA', "Aberto"
    INSCRICOES_E = 'FECHADA', "Fechado"
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
    FINALIZADO = 'FINALIZADO', "Finalizado"


class FormatoTorneio(models.TextChoices):
    SWISS = 'SWISS', 'Sistema Suiço'
    SINGLE_ELIM = 'SINGLE_ELIM', 'Eliminação Simples'


class StatusRodada(models.TextChoices):
    ABERTA = 'AB', 'Aberta'
    FINALIZADA = 'FI', 'Finalizada'
    

class StatusInscricao(models.TextChoices):
    PENDENTE='PE','Pendente'
    APROVADA='AP','Aprovada'
    REJEITADA='RE','Rejeitada'