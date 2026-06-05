from abc import ABC
from matches.enums import StatusPartida


class StatePartida(ABC):
    def __init__(self, partida):
        self.partida = partida

    def iniciar_partida(self):
        raise RuntimeError("Operação inválida")

    def encerrar_partida(self):
        raise RuntimeError("Operação inválida")     


class AgendadaState(StatePartida):
    def iniciar_partida(self):
        self.partida.status = StatusPartida.EM_ANDAMENTO


class AndamentoState(StatePartida):
    def encerrar_partida(self):
        self.partida.status = StatusPartida.FINALIZADA
