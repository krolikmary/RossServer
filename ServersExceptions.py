class ServersExceptions(Exception):
    pass


class ServerAlreadyStartedException(ServersExceptions):
    pass


class IncorrectTSLMessage(ServersExceptions):
    pass