from django.db import transaction
from tournaments.services.rodadaService import RodadaService
from tournaments.services.rankinService import RankingService

class TournamentService:

    @classmethod
    @transaction.atomic
    def iniciar(cls, torneio):
        """Inicia um torneio já gerando os pareamentos
        Args:
            torneio: Torneio a ser iniciado
        """
        torneio.state.iniciar()
        rodada = RodadaService.criar(torneio)
        RodadaService.gerar_pareamentos(rodada)


    @classmethod
    @transaction.atomic
    def proxima_rodada(cls,torneio):
        """Gera uma proxima rodada se não for a ultima
        Caso contrario finaliza o torneio
        Args:
            torneio: Torneio a ser gerada a nova rodada
        Returns:
            Rodada
        """
        
        ultima = torneio.rodadas.last()

        if ultima:
            RodadaService.finalizar(ultima)

        RankingService.recalcular(torneio)

        if torneio.strategy.terminou(torneio):
            cls.finalizar(torneio)
            return None

        rodada = RodadaService.criar(torneio)

        RodadaService.gerar_pareamentos(rodada)

        return rodada


    @classmethod
    def finalizar(cls, torneio):
        """Finaliza o Torneio"""
        torneio.state.finalizar()
