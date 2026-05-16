import json
import os
import logging

class SettingsManager:
    DEFAULT_SETTINGS = {
        "volume_master": 1.0,
        "volume_music": 1.0,
        "volume_sfx": 1.0,
        "screen_shake": True
    }

    def __init__(self, settings_path="settings.json"):
        self.settings_path = settings_path
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except Exception as e:
                logging.error(f"SettingsManager: Failed to load settings from {self.settings_path}: {e}")

    def save(self):
        try:
            with open(self.settings_path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            logging.error(f"SettingsManager: Failed to save settings to {self.settings_path}: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default if default is not None else self.DEFAULT_SETTINGS.get(key))

    def set(self, key, value, save=False):
        self.settings[key] = value
        if save:
            self.save()
