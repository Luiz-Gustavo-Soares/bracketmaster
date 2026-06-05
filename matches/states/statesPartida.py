from abc import ABC
from matches.enums import StatusPartida
from matches.states.exceptions import InsufficientParticipants
from bracketmaster.exceptions import InvalidOption


class StatePartida(ABC):
    def __init__(self, partida):
        self.partida = partida

    def iniciar_partida(self):
        raise InvalidOption("Operação inválida")

    def encerrar_partida(self):
        raise InvalidOption("Operação inválida")     


class AgendadaState(StatePartida):
    def iniciar_partida(self):
        if self.partida.participacoes.count() < 1:
            raise InsufficientParticipants('Partida sem participantes suficientes')
        
        self.partida.status = StatusPartida.EM_ANDAMENTO
        self.partida.save()


class AndamentoState(StatePartida):
    def encerrar_partida(self):
        self.partida.status = StatusPartida.FINALIZADA
        self.partida.save()
