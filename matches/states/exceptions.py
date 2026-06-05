from bracketmaster.exceptions import StateError


class PartidaStateError(StateError):
    pass


# Participantes insuficientes
class InsufficientParticipants(PartidaStateError):
    pass
