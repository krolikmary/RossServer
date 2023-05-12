from enum import Enum


class RossState(Enum):
    OUT = 0
    PVW = 1
    PGM = 2
    BOTH = 3


class RossEvent:
    """

    """
    def __init__(self, camera_id: int, state: RossState):
        self.camera_id = camera_id
        self.state = state

    def __str__(self):
        return f"Camera #{self.camera_id} is {self.state}"

    def get_camera_id(self) -> int:
        return self.camera_id

    def get_camera_state(self) -> int:
        return self.state.value
