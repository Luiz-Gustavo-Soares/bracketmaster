class PartidaError(Exception):
    pass

# Participacao nao pertence a partida
class ParticipatDoesNotInMatchError(PartidaError):
    pass

# Partida já finalizada
class MatchAlreadyFinishedError(PartidaError):
    pass


# Partida não finalizada
class MatchNotFinishedError(PartidaError):
    pass

# Multiplos ganhadores
class MultipleWinnersError(PartidaError):
    pass