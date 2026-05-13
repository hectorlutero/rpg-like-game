import pytest
from src.ui.notifications import NotificationManager

def test_add_notification():
    manager = NotificationManager()
    manager.add("Quest Started!")
    assert len(manager.notifications) == 1
    assert manager.notifications[0]["text"] == "Quest Started!"

def test_notification_timeout():
    manager = NotificationManager(duration=1.0)
    manager.add("Test")
    
    # Update with 0.5s
    manager.update(0.5)
    assert len(manager.notifications) == 1
    
    # Update with another 0.6s (total 1.1s)
    manager.update(0.6)
    assert len(manager.notifications) == 0

def test_multiple_notifications():
    manager = NotificationManager()
    manager.add("First")
    manager.add("Second")
    assert len(manager.notifications) == 2
    
    manager.update(5.0) # Default duration is usually longer
    assert len(manager.notifications) == 0
