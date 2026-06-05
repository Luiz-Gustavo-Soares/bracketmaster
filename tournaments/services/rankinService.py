from typing import List, Dict
from django.db import transaction
from matches.models import Partida
from matches.enums import StatusPartida, ResultadoPartida
from tournaments.models import TorneioParticipante, Torneio


class RankingService:
    """Gerencia o ranking/pontos do torneio"""

    @classmethod
    @transaction.atomic
    def recalcular(cls, torneio: Torneio):
        """Recalcula a pontuacao de cada participante de um torneio 
        levando em consideracao as suas respectivas patidas
        Args:
            torneio: torneio a ser recalculado
        """

        participantes = cls.calcular_ranking(torneio)

        for i, p in enumerate(participantes):
            cls._atualizar_participante(p['participante'], i)

     
    @classmethod
    def _atualizar_participante(cls, participante: TorneioParticipante, posicao: int):

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

        participante.posicao = posicao
        participante.pontos = pontos
        participante.vitorias = wins
        participante.derrotas = losses
        participante.empates = draws

        participante.save()


    @classmethod
    def classificacao(cls, torneio: Torneio):
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


    @classmethod
    def calcular_ranking(cls, torneio: Torneio) -> List[Dict]:
        """Calcula/ordena o ranking levando em consideracao seus pontos e o OMW%
        Args: 
            torneio: Torneio a ser calculado
        Returns:
            Uma lista contendo os participantes ordenados por pontos e OMW%
        """
        participantes = []

        for p in torneio.participantes.all():
            participantes.append({
                "participante": p,
                "pontos": p.pontos,
                "omw": cls.opponent_match_win_percentage(p)
            })

        return sorted(
            participantes,
            key=lambda x: (
                x["pontos"],
                x["omw"]
            ),
            reverse=True
        )


    @classmethod
    def player_winrate(cls, participant: TorneioParticipante) -> float:
        """Calcula a porcentagem de vitoria de um determinado participante
        Args:
            participant: Participante a ser calculado
        Returns:
            winrate do participante
        """
        total = (
            participant.vitorias +
            participant.derrotas +
            participant.empates
        )

        if total == 0:
            return 0

        return (
            participant.vitorias +
            participant.empates * 0.5
        ) / total


    @classmethod
    def opponent_match_win_percentage(cls, participant: TorneioParticipante) -> float:
        """Calcula a media de vitorias dos oponentes de um determinado participante (OMW%)
        Args: 
            participant: Participante do torneio a ser calculado
        Returns: OMW%
        """

        opponents = participant.get_opponents()

        if not opponents:
            return 0

        total = 0

        for opponent in opponents:
            total += max(
                0.33,

                cls.player_winrate(
                    opponent
                )
            )

        return total / len(
            opponents
        )
