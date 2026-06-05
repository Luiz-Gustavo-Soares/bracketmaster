from bracketmaster.exceptions import StateError



class TorneioStateError(StateError):
    pass


# Participantes insuficientes
class InsufficientParticipants(TorneioStateError):
    pass


# Impossivel de finalizar
class ImpossibleToFinish(TorneioStateError):
    pass