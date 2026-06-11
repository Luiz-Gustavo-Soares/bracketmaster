from django.db import models
from matches.enums import StatusPartida, ResultadoPartida
from django.contrib.auth.models import User
from matches.states.statesPartida import StatePartida, AgendadaState, AndamentoState


class Partida(models.Model):
    """Model referente a uma unica partida"""
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices=StatusPartida.choices,
        default=StatusPartida.EM_ANDAMENTO
    )

    jogadores = models.ManyToManyField(
        User,
        through="ParticipacaoPartida"
    )

    rodada = models.ForeignKey(
        'tournaments.Rodada',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='partidas'
    )

    @property
    def state(self) -> StatePartida:
        """Garante que a alteracao do status da Partida seja feita da maneira correta"""

        mapping = {
            StatusPartida.AGENDADA:
                AgendadaState,

            StatusPartida.EM_ANDAMENTO:
                AndamentoState,
        }

        return mapping[
            self.status
        ](self)
    

    def finalizada(self):
        """Verifica se a partida está finalizada"""
        return self.status == StatusPartida.FINALIZADA
    
    def __str__(self):
        return f'Partida {self.id}'
    


class ParticipacaoPartida(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participacoes')
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='participacoes')

    resultado = models.CharField(
        max_length=1,
        choices=ResultadoPartida.choices,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.partida} - {self.jogador}'
