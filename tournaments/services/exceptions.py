class TournamentError(Exception):
    pass

class RegistrationError(TournamentError):
    pass

class RegistrationClosedError(RegistrationError):
    pass

class AlreadyRegisteredError(RegistrationError):
    pass

class ParticipantLimitError(RegistrationError):
    pass

class InvalidCodeError(RegistrationError):
    pass



class RodadaError(Exception):
    pass

class OpenMatchesError(RodadaError):
    pass