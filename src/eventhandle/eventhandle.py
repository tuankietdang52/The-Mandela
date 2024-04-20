from typing import Callable


class EventHandle:
    """
    void function only

    add or remove need tuple[name: str, function]
    """
    def __init__(self):
        self.event_handle: list[tuple[Callable, str]] = list()

    def __iadd__(self, callback: Callable | tuple[Callable, str]):
        if type(callback) is not tuple:
            callback = (callback, " ")

        self.event_handle.append(callback)
        return self

    def __isub__(self, callback: Callable | tuple[Callable, str]):
        if type(callback) is not tuple:
            callback = (callback, " ")

        self.event_handle.remove(callback)
        return self

    def invoke(self):
        """Call all function store in event_handle"""
        for event in self.event_handle:
            event[0]()

    def invoke_specific(self, event_name: str):
        """Call all function with name match event_name"""
        for event in self.event_handle:
            if event[1] == event_name:
                event[0]()
