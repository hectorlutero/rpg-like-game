import pytest
from src.core.juice import JuiceService
from src.core.settings import SettingsManager

def test_juice_respects_screen_shake_setting():
    settings = SettingsManager("test_juice_settings.json")
    juice = JuiceService(settings_manager=settings)
    
    # Enable screen shake
    settings.set("screen_shake", True)
    juice.shake(0.5)
    assert juice.trauma > 0
    
    # Reset trauma
    juice.trauma = 0
    
    # Disable screen shake
    settings.set("screen_shake", False)
    juice.shake(0.5)
    assert juice.trauma == 0

import os
if os.path.exists("test_juice_settings.json"):
    os.remove("test_juice_settings.json")
