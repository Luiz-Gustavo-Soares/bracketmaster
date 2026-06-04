from django.db import transaction
from tournaments.models import Rodada
from tournaments.enums import StatusRodada
from matches.enums import StatusPartida
from tournaments.services.exceptions import OpenMatchesError

class RodadaService:

    @classmethod
    @transaction.atomic
    def criar(cls, torneio):
        """Cria uma nova Rodada para um torneio
        Args:
            torneio: Torneio a ser criada a rodada
        """
        numero = torneio.rodadas.count() + 1

        rodada = Rodada.objects.create(
            torneio=torneio,
            numero=numero
        )

        return rodada
    

    @classmethod
    @transaction.atomic
    def gerar_pareamentos(cls, rodada):
        """Gera os pareamentos para a rodada
        Args:
            rodada: Rodada a ser gereada os pareamentos
        """
        torneio = rodada.torneio

        torneio.strategy.gerar_pareamento(rodada)
        rodada.save()


    @classmethod
    @transaction.atomic
    def finalizar(cls, rodada):
        """Finaliza uma rodada
        Para finalizar verifica se a rodada em questao está com um status valido (caso contrario: RuntimeError)
        Args:
            rodada: Rodada a ser finalizada
        """
        abertas = rodada.partidas.filter(
            status__in=[
                StatusPartida.AGENDADA,
                StatusPartida.EM_ANDAMENTO
            ]
        ).exists()

        if abertas:
            raise OpenMatchesError("Existem partidas abertas")

        rodada.status = (
            StatusRodada.FINALIZADA
        )

        rodada.save()
