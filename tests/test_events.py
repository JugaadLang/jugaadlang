import pytest
from jugaadlang.events.bus import EventBus

def test_event_bus_singleton():
    bus1 = EventBus()
    bus2 = EventBus()
    assert bus1 is bus2

def test_event_bus_subscribe_emit():
    bus = EventBus()
    bus.clear()

    data_received = []

    def callback(data):
        data_received.append(data)

    bus.subscribe("TEST_EVENT", callback)
    bus.emit("TEST_EVENT", {"key": "value"})

    assert len(data_received) == 1
    assert data_received[0]["key"] == "value"

def test_event_bus_unsubscribe():
    bus = EventBus()
    bus.clear()

    data_received = []

    def callback(data):
        data_received.append(data)

    bus.subscribe("TEST_EVENT", callback)
    bus.unsubscribe("TEST_EVENT", callback)
    bus.emit("TEST_EVENT", {"key": "value"})

    assert len(data_received) == 0

def test_event_bus_error_handling():
    bus = EventBus()
    bus.clear()

    def callback_error(data):
        raise ValueError("Oops")

    data_received = []
    def callback_ok(data):
        data_received.append(data)

    bus.subscribe("TEST_EVENT", callback_error)
    bus.subscribe("TEST_EVENT", callback_ok)
    
    # Should not raise exception
    bus.emit("TEST_EVENT", {"key": "value"})
    
    # callback_ok should still have been called (assuming order) or at least doesn't crash
    # EventBus uses a list, so order is preserved. callback_error raises, but it is caught.
    assert len(data_received) == 1
