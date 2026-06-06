from core.exceptions import StateError



class TorneioStateError(StateError):
    pass


# Participantes insuficientes
class InsufficientParticipantsError(TorneioStateError):
    pass


# Impossivel de finalizar
class ImpossibleToFinishError(TorneioStateError):
    pass