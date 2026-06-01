from abc import ABC, abstractmethod



class BaseStrategy(ABC):
    """Classe pai para gerir diferentes formatos de torneio"""

    def __init__(self, torneio):
        self.torneio = torneio

    @abstractmethod
    def gerar_pareamento(self, rodada):
        pass

    @abstractmethod
    def pode_criar_proxima_rodada(self):
        pass

    @abstractmethod
    def finalizar_rodada(self):
        pass

    @abstractmethod
    def terminou(self):
        pass
