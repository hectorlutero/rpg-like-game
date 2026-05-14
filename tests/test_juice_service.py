import pytest
from src.core.juice import JuiceService

def test_juice_service_init():
    service = JuiceService()
    assert service.trauma == 0.0
    assert service.flash_alpha == 0

def test_juice_shake():
    service = JuiceService()
    service.shake(0.5)
    assert service.trauma == 0.5
    service.update(0.1)
    assert service.trauma < 0.5

def test_juice_hit_stop():
    service = JuiceService()
    service.hit_stop(0.2)
    assert service.hit_stop_time == 0.2
    
    # Simulate update with dt=0.1
    service.update(0.1)
    assert service.hit_stop_time == 0.1
    # Check if logic freeze is requested
    assert service.is_hit_stopping()
    
    service.update(0.2) # Should finish hit stop
    assert not service.is_hit_stopping()
