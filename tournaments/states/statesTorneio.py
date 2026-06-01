from abc import ABC


class StateTorneio(ABC):
    def __init__(self, torneio):
        self.torneio = torneio

    def abrir_inscricoes(self):
        raise RuntimeError("Operação inválida")

    def encerrar_inscricoes(self):
        raise RuntimeError("Operação inválida")     
    
    def iniciar(self):
        raise RuntimeError("Operação inválida")     

    def finalizar(self):
        raise RuntimeError("Operação inválida")


class CriadoState(StateTorneio):
    pass

class InscricoesState(StateTorneio):
    pass

class EncInscricoesState(StateTorneio):
    pass

class EmAndamentoState(StateTorneio):
    pass
