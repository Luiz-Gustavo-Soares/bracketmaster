class StateError(Exception):
    pass

# Opcao invalida
class InvalidOptionError(StateError):
    pass


class PermissionDenied(Exception):
    pass