class PartidaStateError(Exception):
    pass

# Opcao invalida
class InvalidOption(PartidaStateError):
    pass


# Participantes insuficientes
class InsufficientParticipants(PartidaStateError):
    pass
