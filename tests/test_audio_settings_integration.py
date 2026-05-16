import pytest
import os
import pygame
from src.core.audio import SoundManager
from src.core.settings import SettingsManager

SETTINGS_FILE = "test_audio_settings.json"

@pytest.fixture
def clean_settings():
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)
    yield
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)

def test_sound_manager_loads_from_settings(clean_settings):
    # Prepare settings
    settings = SettingsManager(SETTINGS_FILE)
    settings.set("volume_master", 0.3)
    settings.set("volume_music", 0.5)
    settings.save()
    
    # Init SoundManager with these settings
    manager = SoundManager(settings_manager=settings)
    
    assert manager.get_volume("master") == 0.3
    assert manager.get_volume("music") == 0.5

def test_sound_manager_persists_on_set_volume(clean_settings):
    settings = SettingsManager(SETTINGS_FILE)
    manager = SoundManager(settings_manager=settings)
    
    manager.set_volume("master", 0.8)
    
    # Reload settings to check persistence
    new_settings = SettingsManager(SETTINGS_FILE)
    assert new_settings.get("volume_master") == 0.8
