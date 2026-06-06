from abc import ABC
from tournaments.enums import StatusTorneio
from tournaments.states.exceptions import ImpossibleToFinishError, InsufficientParticipantsError
from core.exceptions import InvalidOptionError

class StateTorneio(ABC):
    def __init__(self, torneio):
        self.torneio = torneio

    def abrir_inscricoes(self):
        raise InvalidOptionError("Operação inválida")

    def encerrar_inscricoes(self):
        raise InvalidOptionError("Operação inválida")     
    
    def iniciar(self):
        raise InvalidOptionError("Operação inválida")     

    def finalizar(self):
        raise InvalidOptionError("Operação inválida")
    
    def wipe(self):
        """Reseta o status do torneio para criado"""
        self.torneio.status = StatusTorneio.CRIADO
        self.torneio.save()


class CriadoState(StateTorneio):
    def abrir_inscricoes(self):
        """Altera o status do torneio para receber INSCRICOES"""

        self.torneio.status = StatusTorneio.INSCRICOES
        self.torneio.save()


class InscricoesState(StateTorneio):
    def encerrar_inscricoes(self):
        """Altera o status do torneio para INSCRICOES_ENCERRADAS 
        somente se tiver 2 ou mais inscritos"""

        if self.torneio.participantes.count() < 2:
            raise InsufficientParticipantsError("Poucos participantes")

        self.torneio.status = StatusTorneio.INSCRICOES_E
        self.torneio.save()


class EncInscricoesState(StateTorneio):
    def iniciar(self):
        """Altera o status do torneio para EM_ANDAMENTO"""

        self.torneio.status = StatusTorneio.EM_ANDAMENTO
        self.torneio.save()


class EmAndamentoState(StateTorneio):
    def finalizar(self):
        if not self.torneio.strategy.terminou():
            raise ImpossibleToFinishError("Rodadas abertas")

        self.torneio.status = StatusTorneio.FINALIZADO
        self.torneio.save()
