from django.db import transaction
from matches.models import Partida
from matches.enums import StatusPartida, ResultadoPartida


class RankingService:
    """Gerencia o ranking/pontos do torneio"""

    @classmethod
    @transaction.atomic
    def recalcular(cls, torneio):
        """Recalcula o ranking de cada participante de um torneio 
        levando em consideracao as suas respectivas patidas
        Args:
            torneio: torneio a ser recalculado
        """

        participantes = torneio.participantes.all()

        for p in participantes:
            cls._atualizar_participante(p)

     
    @classmethod
    def _atualizar_participante(cls, participante):

        partidas = Partida.objects.filter(
            rodada__torneio=participante.torneio,
            participacoes__jogador=participante.jogador,
            status=StatusPartida.FINALIZADA
        )

        pontos = 0
        wins = 0
        losses = 0
        draws = 0


        for partida in partidas:

            participacao = (
                partida.participacoes.get(
                    jogador=participante.jogador
                )
            )

            resultado = participacao.resultado

            if resultado == ResultadoPartida.VITORIA:
                wins += 1
                pontos += 3

            elif resultado == ResultadoPartida.EMPATE:
                draws += 1
                pontos += 1

            else:
                losses += 1

        participante.pontos = pontos
        participante.vitorias = wins
        participante.derrotas = losses
        participante.empates = draws

        participante.save()


    @classmethod
    def classificacao(cls, torneio):
        """Classifica os participantes do torneio por meio dos pontos e vitorias
        Args:
            torneio: Torneio a ser classificado
        Returns:
            Participantes do torneio ordenado
        """
        return (
            torneio.participantes
            .order_by(
                '-pontos',
                '-vitorias'
            )
        )
