from enum import Enum

from MessagersInterfaces import Listener, Notifier, T
from ServerConfig import ServerConfig
from UMDDecoder import TSLEvent


class RossState(Enum):
    OUT = 0
    PVW = 1
    PGM = 2
    BOTH = 3


class RossEvent:
    def __init__(self, camera_id: int, state: RossState):
        self.camera_id = camera_id
        self.state = state

    def __str__(self):
        return f"Camera #{self.camera_id} is {self.state}"

    def get_camera_id(self) -> int:
        return self.camera_id

    def get_camera_state(self) -> int:
        return self.state.value


def umd_to_ross_event(umd_msg: TSLEvent) -> RossEvent:
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
