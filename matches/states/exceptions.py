from core.exceptions import StateError


class PartidaStateError(StateError):
    pass


# Participantes insuficientes
class InsufficientParticipantsError(PartidaStateError):
    pass
