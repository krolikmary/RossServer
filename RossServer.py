from MessagersInterfaces import Listener, Notifier
from RossEvent import RossState, RossEvent
from UMDDecoder import TSLEvent


def umd_to_ross_event(umd_msg: TSLEvent) -> RossEvent:
    """
        function that converts TSLEvent to RossEvent
    """
    is_pgm = umd_msg.tallies[1]
    is_pvw = umd_msg.tallies[0]
    if is_pgm:
        if is_pvw:
            state = RossState.BOTH
        else:
            state = RossState.PGM
    else:
        if is_pvw:
            state = RossState.PVW
        else:
            state = RossState.OUT

    return RossEvent(umd_msg.cameraNum, state)


class RossDecoder(Listener[TSLEvent], Notifier[RossEvent]):

    def __init__(self, listener: Listener[RossEvent]):
        self._listener = listener

    def on_message(self, message: TSLEvent, notifier: Notifier[TSLEvent]):
        self._listener(umd_to_ross_event(message), self)
