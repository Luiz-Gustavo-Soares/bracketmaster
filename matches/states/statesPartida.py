from abc import ABC
from matches.enums import StatusPartida
from matches.states.exceptions import InsufficientParticipantsError
from bracketmaster.exceptions import InvalidOptionError


class StatePartida(ABC):
    def __init__(self, partida):
        self.partida = partida

    def iniciar_partida(self):
        raise InvalidOptionError("Operação inválida")

    def encerrar_partida(self):
        raise InvalidOptionError("Operação inválida")     


class AgendadaState(StatePartida):
    def iniciar_partida(self):
        if self.partida.participacoes.count() < 1:
            raise InsufficientParticipantsError('Partida sem participantes suficientes')
        
        self.partida.status = StatusPartida.EM_ANDAMENTO
        self.partida.save()


class AndamentoState(StatePartida):
    def encerrar_partida(self):
        self.partida.status = StatusPartida.FINALIZADA
        self.partida.save()
