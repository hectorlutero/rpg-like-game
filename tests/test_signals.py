import pytest
from src.core.signals import SignalBus

def test_signal_emission_reaches_subscriber():
    bus = SignalBus()
    received = []
    
    def on_event(data):
        received.append(data)
        
    bus.subscribe("test_event", on_event)
    bus.emit("test_event", payload="hello")
    
    assert len(received) == 1
    assert received[0]["payload"] == "hello"

def test_multiple_subscribers():
    bus = SignalBus()
    count = 0
    
    def increment(_):
        nonlocal count
        count += 1
        
    bus.subscribe("event", increment)
    bus.subscribe("event", increment)
    bus.emit("event")
    
    assert count == 2

def test_unsubscribe():
    bus = SignalBus()
    received = []
    
    def on_event(data):
        received.append(data)
        
    bus.subscribe("test", on_event)
    bus.unsubscribe("test", on_event)
    bus.emit("test")
    
    assert len(received) == 0

def test_subscribe_all():
    bus = SignalBus()
    received = []
    
    def on_any(data):
        received.append(data)
        
    bus.subscribe_all(on_any)
    bus.emit("type1", val=1)
    bus.emit("type2", val=2)
    
    assert len(received) == 2
    assert received[0]["type"] == "type1"
    assert received[1]["type"] == "type2"
