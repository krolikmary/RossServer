from enum import Enum

from MessagersInterfaces import Listener, Notifier, T
from RossServer import *
from UMDDecoder import *


class Filter(Listener[RossEvent], Notifier[RossEvent]):

    def __init__(self, listener: Listener[RossEvent], filter_plenty: set[int]):
        self._listener = listener
        self._plenty_of_cams = filter_plenty.copy()

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        """
        Receives a set of necessary cameras at the input and checks whether
        the switched camera is included in this set,
        if it is included, it sends a message about its change
        Param: RossState
        Notifies: RossState
        """
        len_of_set = len(self._plenty_of_cams)
        if message.get_camera_id() in self._plenty_of_cams:
            self._listener(message, self)
