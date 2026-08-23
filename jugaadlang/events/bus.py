from typing import Callable, Any, Dict, List

class EventBus:
    """
    A simple singleton event bus for decoupling core modules (Lexer, Parser, Runtime)
    using the observer pattern.
    """
    _instance = None

    def __new__(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe a callback to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Unsubscribe a callback from a specific event type."""
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]

    def emit(self, event_type: str, data: Dict[str, Any] = None) -> None:
        """Emit an event to all subscribed callbacks."""
        if data is None:
            data = {}
        
        # We use a copy of the list so that if a subscriber modifies the list,
        # it doesn't break the current iteration.
        callbacks = list(self._subscribers.get(event_type, []))
        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                # Event callbacks should not break the main execution flow
                pass

    def clear(self) -> None:
        """Clear all subscribers (mostly used for testing)."""
        self._subscribers.clear()


# Global event bus instance
event_bus = EventBus()
