class SignalBus:
    def __init__(self):
        self._subscribers = {}
        self._global_subscribers = []

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def subscribe_all(self, callback):
        self._global_subscribers.append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
        if callback in self._global_subscribers:
            self._global_subscribers.remove(callback)

    def emit(self, event_type, **kwargs):
        # Notify specific subscribers
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(kwargs)
        
        # Notify global subscribers
        data = kwargs.copy()
        data["type"] = event_type
        for callback in self._global_subscribers:
            callback(data)
