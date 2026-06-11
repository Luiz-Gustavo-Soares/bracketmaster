from django.db import transaction
from django.contrib.auth.models import User
from tournaments.enums import StatusInscricao
from tournaments.models import TorneioParticipante, Torneio
from tournaments.services.rodadaService import RodadaService
from tournaments.services.rankinService import RankingService
from core.exceptions import PermissionDenied
from tournaments.services.exceptions import RegistrationClosedError, AlreadyRegisteredError,\
                                            ParticipantLimitError, InvalidCodeError


class TournamentRegistrationService:

    @classmethod
    @transaction.atomic
    def adicionar_jogador(cls, torneio: Torneio, jogador: User, codigo: str = None):
        """Adiciona um jogador em um torneio
        Args:
            torneio: Torneio
            jogador: User a ser inserido
            codigo: str contendo o codigo para se inscrever
        """

        if not torneio.inscricoes_abertas():
            raise RegistrationClosedError('Fora da etapa de inscrição')
        
        if TorneioParticipante.objects.filter(torneio=torneio, jogador=jogador).exists():
            raise AlreadyRegisteredError('Já inscrito')
        
        if TorneioParticipante.objects.filter(torneio=torneio).count() >= torneio.numero_maximo_participantes:
            raise ParticipantLimitError('Limte de participantes atingido')

        if not torneio.inscricao_publica:
            if torneio.codigo_inscricao != codigo:
                raise InvalidCodeError('Codigo Invalido')

        TorneioParticipante.objects.create(torneio=torneio, jogador=jogador)
        

    @classmethod
    @transaction.atomic
    def approvar_jogador(cls, participante: TorneioParticipante, organizador: User):

        if participante.torneio.organizador != organizador:
            raise PermissionDenied()

        participante.status = StatusInscricao.APROVADA

        participante.save()


    @classmethod
    @transaction.atomic
    def regeitar_jogador(cls, participante: TorneioParticipante, organizador: User):

        if participante.torneio.organizador != organizador:
            raise PermissionDenied()

        participante.status = StatusInscricao.REJEITADA

        participante.save()
