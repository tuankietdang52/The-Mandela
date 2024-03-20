class EventHandle:
    """void only"""
    def __init__(self):
        self.event_handle = []

    def __iadd__(self, event):
        self.event_handle.append(event)
        return self

    def __isub__(self, event):
        self.event_handle.remove(event)
        return self

    def invoke(self):
        """Call all function store in event_handle"""
        for event in self.event_handle:
            event()
