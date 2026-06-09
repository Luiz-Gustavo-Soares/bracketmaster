from django.db import models
import secrets
from random import choice
from tournaments.enums import FormatoJogo, TipoTorneio, FormatoTorneio, StatusTorneio, StatusRodada, StatusInscricao, Fundos
from django.contrib.auth.models import User

from .strategies.singleEliminationStrategy import SingleEliminationStrategy
from .strategies.swissStrategy import SwissStrategy
from .strategies.base_strategy import BaseStrategy

from .states.statesTorneio import EncInscricoesState, EmAndamentoState, CriadoState, InscricoesState, StateTorneio
from matches.models import Partida
from core.models import Cidade


class Torneio(models.Model):
    """Modelo Principal do torneio"""

    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)

    organizador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='torneios_criados'
    )
    
    imagem_fundo = models.CharField(
        max_length=20,
        choices=Fundos
    )

    numero_maximo_participantes = models.PositiveIntegerField(default=20)

    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    codigo_inscricao = models.CharField(
        max_length=10,
        editable=False
    )

    inscricao_publica = models.BooleanField(
        default=True
    )

    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.PROTECT,
        related_name='torneios',
        null=True,
        blank=True
    )

    local = models.CharField(max_length=150)

    premiacoes = models.TextField(blank=True, null=True)

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
    

    @staticmethod
    def gerar_codigo() -> str:
        """Gera um token de 6 digitos hexadecimal"""
        codigo = secrets.token_hex(3).upper()
        return codigo
    

    def get_premiacoes_list(self) -> list:
        """Retorna uma lista contendo as premiacoes divididas em: 1°, 2°, 3° outro...
        """
        return self.premiacoes.strip().split('\n', 3)


    def inscricoes_abertas(self):
        """Verifica se o status do torneio aceita inscricoes"""
        return self.status == StatusTorneio.INSCRICOES


    def adicionar_cidade(self, cidade_text: str, estado_text: str):
        """Adicionar uma relacao para o campo cidade
        Obs. Não salva, somente atribui

        Args: 
            cidade_text: nome da cidade
            estado_text: estado da cidade
        """
        cidade, _ = Cidade.objects.get_or_create(
                nome=Cidade._normalizar(cidade_text),
                estado=Cidade._normalizar(estado_text)
            )
        
        self.cidade = cidade


    def get_fundo_path(self):
        return f"/static/media/capas_campeonato/{self.avatar}.jpg"


    def save(self, *args, **kwargs):

        if not self.codigo_inscricao:
            self.codigo_inscricao = (
                self.gerar_codigo()
            )

        if not self.imagem_fundo:
            self.imagem_fundo = choice(Fundos.values)

        super().save(*args, **kwargs)



    def __str__(self):
        return self.nome


class ParticipanteQuerySet(models.QuerySet):
    def aprovados(self):
        return self.filter(
            status=StatusInscricao.APROVADA
        )


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

    status = models.CharField(
        max_length=2,
        choices=StatusInscricao,
        default=StatusInscricao.PENDENTE
    )

    objects = ParticipanteQuerySet.as_manager()

    pontos = models.IntegerField(default=0)

    vitorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)

    posicao = models.PositiveIntegerField(default=0)

    data_inscricao = models.DateTimeField(
        auto_now_add=True
    )
    

    def get_opponents(self):
        """Busca todos os oponentes do participante"""

        opponents = []

        partidas = Partida.objects.filter(
            participacoes__jogador=self.jogador,
            rodada__torneio=self.torneio
        )

        for partida in partidas:

            participacoes = (
                partida.participacoes.exclude(
                    jogador=self.jogador
                )
            )

            for p in participacoes:
                opponents.append(
                    TorneioParticipante.objects.get(
                        torneio=self.torneio,
                        jogador=p.jogador
                    )
                )

        return opponents
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'torneio',
                    'jogador'
                ],

                name='participante_unico'
            )
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

        ordering = ['-numero']
