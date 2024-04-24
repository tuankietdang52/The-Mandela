from typing import Callable
from src.eventhandle.argument.eventargument import *


class EventHandle:
    """
    add or remove need tuple[function, args: event argument]
    """
    def __init__(self):
        self.event_handle: list[tuple[Callable, EventArgs]] = list()

    def __iadd__(self, callback: tuple[Callable, EventArgs]):
        self.event_handle.append(callback)
        return self

    def __isub__(self, callback: tuple[Callable, EventArgs]):
        self.event_handle.remove(callback)
        return self

    def invoke(self):
        """Call all function store in event_handle"""
        for event in self.event_handle:
            callback = event[0]
            args = event[1]

            callback(args)
