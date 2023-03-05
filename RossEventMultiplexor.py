import threading
from typing import List, Set

from MessagersInterfaces import Listener, T, Notifier
from RossServer import RossEvent


class Multiplexor(Listener[RossEvent], Notifier[RossEvent]):
    """
        class that listens to one Listener[RossEvent] and notifies multiple Listeners[RossEvent]
    """
    def __init__(self):
        self._listenerSet: Set[Listener[RossEvent]] = set()
        self._listMutex = threading.Lock()

    def add_listener(self, listener: Listener[RossEvent]):
        """
        add a listener that will be notified by the multiplexor

        :param listener: listener to add
        :type listener: Listener[RossEvent]
        """
        with self._listMutex:
            self._listenerSet.add(listener)

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        with self._listMutex:
            for listener in self._listenerSet:
                listener(message, self)

    def get_listeners(self) -> Set[Listener[RossEvent]]:
        """
        :return: set of listener that multiplexor notifies
        """
        with self._listMutex:
            return self._listenerSet.copy()

    def delete_listener(self, listener: Listener[RossEvent]):
        """
        removes listener from set of listeners to be notified

        :param listener: listener to not notify anymore
        :return:
        """
        with self._listMutex:
            self._listenerSet.remove(listener)
