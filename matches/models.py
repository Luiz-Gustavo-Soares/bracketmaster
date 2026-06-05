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
        default=StatusPartida.AGENDADA
    )

    jogadores = models.ManyToManyField(
        User,
        through="ParticipacaoPartida"
    )

    rodada = models.ForeignKey(
        'tournaments.Rodada',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
    
    
    def _get_ganhador(self):
        """
        Retorna (se ouver) o ganhador da Partida
        Returns:
            User: usuario ganhador
        """
        if self.status != StatusPartida.FINALIZADA:
            raise RuntimeError('Partida ainda nao finalizada')

        participacao = self.participacoes.filter(
            resultado=ResultadoPartida.VITORIA
        ).first()

        if participacao:
            return participacao.jogador

        return None
    

    def get_resultado(self):
        """
        Retorna o resultado da partida
        Returns:
            Tuple: 
                (
                    ResultadoPartida, 
                    ganhador (se ouver)
                )
        """
        if self.status != StatusPartida.FINALIZADA:
            return None

        ganhador = self._get_ganhador()

        if ganhador:
            return ResultadoPartida.VITORIA, ganhador

        return ResultadoPartida.EMPATE, None


    
    def finalizar_partida(self, winner: User = None):
        """Finaliza a partida
        Calcula/Peenche o resultado de cada participante
        Args:
            winner: User 
                o ganhador da partida (se ouver). defalt -> None
        """
        if self.status == StatusPartida.FINALIZADA:
            raise RuntimeError('Partida já finalizada')
        
        participacoes = self.participacoes.all()

        if winner and not participacoes.filter(jogador=winner).exists():
            raise RuntimeError('O vencedor nao pertence a partida')

        if self.participacoes.count() < 1:
            raise RuntimeError('Partida sem participantes suficientes')
        

        for participante in participacoes:

            if winner and participante.jogador == winner:
                participante.resultado = ResultadoPartida.VITORIA

            elif winner:
                participante.resultado = ResultadoPartida.DERROTA

            else:
                participante.resultado = ResultadoPartida.EMPATE

            participante.save()

        self.status = StatusPartida.FINALIZADA
        self.save()


    def __str__(self):
        return f'Partida {self.id}'
    


class ParticipacaoPartida(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='participacoes')

    resultado = models.CharField(
        max_length=1,
        choices=ResultadoPartida.choices,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Participacao {self.partida} - {self.jogador}'
