from django.db import transaction
from django.contrib.auth.models import User
from tournaments.enums import StatusTorneio
from tournaments.models import TorneioParticipante, Torneio
from tournaments.services.rodadaService import RodadaService
from tournaments.services.rankinService import RankingService
from tournaments.services.exceptions import RegistrationClosedError, AlreadyRegisteredError,\
                                            ParticipantLimitError, InvalidCodeError

class TournamentService:

    @classmethod
    @transaction.atomic
    def abrir_inscricoes(cls, torneio: Torneio):
        """Inicia o periodo de inscricoes
        Args: 
            torneio: Torneio"""
        
        torneio.state.abrir_inscricoes()
 

    @classmethod
    @transaction.atomic
    def encerrar_inscricoes(cls, torneio: Torneio):
        """Ecerra o periodo de inscrições
        Args: 
            torneio: Torneio"""
            
        torneio.state.encerrar_inscricoes()


    @classmethod
    @transaction.atomic
    def iniciar(cls, torneio: Torneio):
        """Inicia um torneio já gerando os pareamentos
        Args:
            torneio: Torneio a ser iniciado
        """

        torneio.state.iniciar()
        rodada = RodadaService.criar(torneio)
        RodadaService.gerar_pareamentos(rodada)


    @classmethod
    @transaction.atomic
    def proxima_rodada(cls, torneio: Torneio):
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

        if torneio.strategy.terminou():
            cls.finalizar(torneio)
            return None

        rodada = RodadaService.criar(torneio)

        RodadaService.gerar_pareamentos(rodada)

        return rodada


    @classmethod
    @transaction.atomic
    def finalizar(cls, torneio: Torneio):
        """Finaliza o Torneio
        Args: 
            torneio: Torneio"""
        
        torneio.state.finalizar()
