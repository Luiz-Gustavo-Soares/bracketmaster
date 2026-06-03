from django.db import models
from .enums import FormatoJogo, TipoTorneio, FormatoTorneio, StatusTorneio, StatusRodada
from django.contrib.auth.models import User

from .strategies.singleEliminationStrategy import SingleEliminationStrategy
from .strategies.swissStrategy import SwissStrategy
from .strategies.base_strategy import BaseStrategy

from .states.statesTorneio import EncInscricoesState, EmAndamentoState, CriadoState, InscricoesState, StateTorneio

class Torneio(models.Model):
    """Modelo Principal do torneio"""

    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)

    organizador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='torneios_criados'
    )

    tipo = models.CharField(
        max_length=2,
        choices=TipoTorneio.choices,
        default=TipoTorneio.COMPETITIVO
    )

    formato_torneio = models.CharField(
        max_length=20,
        choices=FormatoTorneio.choices
    )

    status = models.CharField(
        max_length=21,
        choices=StatusTorneio.choices,
        default=StatusTorneio.CRIADO
    )

    formato_jogo = models.CharField(
        max_length=2,
        choices=FormatoJogo.choices,
        default=FormatoJogo.COMMANDER
    )

    numero_rodadas = models.PositiveIntegerField()

    data_inicio = models.DateTimeField()

    criado_em = models.DateTimeField(auto_now_add=True)


    @property
    def strategy(self) -> BaseStrategy:
        """Altera a estrategia conforme o FORMATO do TORNEIO"""
        mapping = {

            FormatoTorneio.SWISS:
                SwissStrategy,

            FormatoTorneio.SINGLE_ELIM:
                SingleEliminationStrategy
        }

        return mapping[
            self.formato_torneio
        ](self)
    

    @property
    def state(self) -> StateTorneio:
        """Garante que a alteracao do status do torneio seja feita da maneira correta"""

        mapping = {

            StatusTorneio.CRIADO:
                CriadoState,

            StatusTorneio.INSCRICOES:
                InscricoesState,

            StatusTorneio.INSCRICOES_E:
                EncInscricoesState,

            StatusTorneio.EM_ANDAMENTO:
                EmAndamentoState
        }

        return mapping[
            self.status
        ](self)

    def __str__(self):
        return self.nome

class TorneioParticipante(models.Model):
    """Modelo responsavel de registrar jogadores no torneio"""

    torneio = models.ForeignKey(
        Torneio,
        on_delete=models.CASCADE,
        related_name='participantes'
    )

    jogador = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    pontos = models.IntegerField(default=0)

    vitorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            ('torneio', 'jogador')
        ]
    
    def __str__(self):
        return f'{self.torneio} - {self.jogador}'

class Rodada(models.Model):
    """Modelo responsavel por cada rodada do torneio"""

    torneio = models.ForeignKey(
        Torneio,
        on_delete=models.CASCADE,
        related_name='rodadas'
    )

    numero = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=StatusRodada.choices,
        default=StatusRodada.ABERTA
    )

    criada_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = [
            ('torneio', 'numero')
        ]

        ordering = ['numero']
