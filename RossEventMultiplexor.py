import threading
from typing import List

from MessagersInterfaces import Listener, T, Notifier
from RossServer import RossEvent


class Multiplexor(Listener[RossEvent], Notifier[RossEvent]):
    def __init__(self):
        self._listenerList: List[Listener[RossEvent]] = []
        self._listMutex = threading.Lock()

    def add_listener(self, listener: Listener[RossEvent]):
        with self._listMutex:
            self._listenerList.append(listener)
            return len(self._listenerList) - 1

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        with self._listMutex:
            for listener in self._listenerList:
                listener(message, self)

    def get_listeners(self):
        with self._listMutex:
            return self._listenerList.copy()

    def delete_listener_by_id(self, index: int) -> Listener[RossEvent]:
        with self._listMutex:
            return self._listenerList.pop(index)

    def delete_listener(self, listener: Listener[RossEvent]):
        with self._listMutex:
            self._listenerList.remove(listener)
