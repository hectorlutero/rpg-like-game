import pytest
import os
import json
from src.core.settings import SettingsManager

SETTINGS_FILE = "test_settings.json"

@pytest.fixture
def settings_manager():
    # Ensure clean state
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)
    
    manager = SettingsManager(SETTINGS_FILE)
    yield manager
    
    # Cleanup
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)

def test_default_settings(settings_manager):
    assert settings_manager.get("volume_master") == 1.0
    assert settings_manager.get("volume_music") == 1.0
    assert settings_manager.get("volume_sfx") == 1.0
    assert settings_manager.get("screen_shake") is True

def test_set_and_get_setting(settings_manager):
    settings_manager.set("volume_master", 0.5)
    assert settings_manager.get("volume_master") == 0.5
    
    settings_manager.set("screen_shake", False)
    assert settings_manager.get("screen_shake") is False

def test_persistence(settings_manager):
    settings_manager.set("volume_master", 0.7)
    settings_manager.set("screen_shake", False)
    settings_manager.save()
    
    # Create a new manager pointing to the same file
    new_manager = SettingsManager(SETTINGS_FILE)
    assert new_manager.get("volume_master") == 0.7
    assert new_manager.get("screen_shake") is False

def test_auto_save(settings_manager):
    # If we want auto-save on set
    settings_manager.set("volume_music", 0.2, save=True)
    
    new_manager = SettingsManager(SETTINGS_FILE)
    assert new_manager.get("volume_music") == 0.2
