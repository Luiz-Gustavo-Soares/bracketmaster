class PartidaError(Exception):
    pass

# Participacao nao pertence a partida
class ParticipatDoesNotInMatch(PartidaError):
    pass

# Partida já finalizada
class MatchAlreadyFinished(PartidaError):
    pass


# Partida não finalizada
class MatchNotFinished(PartidaError):
    pass

# Multiplos ganhadores
class MultipleWinners(PartidaError):
    pass