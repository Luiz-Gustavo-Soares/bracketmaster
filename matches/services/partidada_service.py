from django.db import transaction
from matches.models import Partida, ParticipacaoPartida
from matches.enums import ResultadoPartida, StatusPartida
from matches.services.exceptions import ParticipatDoesNotInMatchError, MatchAlreadyFinishedError, MatchNotFinishedError, MultipleWinnersError


class PartidaService:

    @classmethod
    @transaction.atomic
    def iniciar_partida(cls, partida: Partida):
        """Inicia uma Partida
        Args: 
            partida: Partida
        """
        partida.state.iniciar_partida()


    @classmethod
    @transaction.atomic
    def finalizar_partida(cls, partida: Partida):
        """Finaliza uma Partida
        Args: 
            partida: Partida
        """
        if partida.status == StatusPartida.EM_ANDAMENTO:
            partida.state.encerrar_partida()


    @classmethod
    @transaction.atomic
    def registrar_resultado(
            cls, 
            partida: Partida, 
            participacao_vencedora: ParticipacaoPartida=None
        ):
        """Registra o resultado de uma partida
        Se o resultado da partida for EMPATE a participacao_vencedora deve constar None
        Args: 
            partida: Partida
            participacao_vencedora: ParticipacaoPartida=None
        """

        if participacao_vencedora is not None:
            if participacao_vencedora.partida.id != partida.id:
                raise ParticipatDoesNotInMatchError("Participação não pertence à partida")
            

        # if partida.finalizada():
        #     raise MatchAlreadyFinishedError('Partida já finalizada')

          
        participacoes = list(partida.participacoes.all())

        for participante in participacoes:

            if participacao_vencedora and participante == participacao_vencedora:
                participante.resultado = ResultadoPartida.VITORIA

            elif participacao_vencedora:
                participante.resultado = ResultadoPartida.DERROTA

            else:
                participante.resultado = ResultadoPartida.EMPATE


        ParticipacaoPartida.objects.bulk_update(
            participacoes,
            ['resultado']
        )


    @classmethod
    def ganhador(cls, partida: Partida) -> ParticipacaoPartida:
        """Busca o ganhador de uma determinada partida
        Returns: 
            ParticipacaoPartida ou None caso EMPATE
        """
        if not partida.finalizada():
            raise MatchNotFinishedError("Partida ainda nao finalizada")
        
        vencedores = partida.participacoes.filter(
            resultado=ResultadoPartida.VITORIA
        )

        if vencedores.count() > 1:
            raise MultipleWinnersError(
                "Partida possui múltiplos vencedores"
            )

        return vencedores.first()
