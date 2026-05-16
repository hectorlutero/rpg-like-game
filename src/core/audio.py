import pygame
import logging
import os
import json

class SoundManager:
    def __init__(self, config_path=None, settings_manager=None):
        self.enabled = False
        self.current_track = None
        self.current_ambient = None
        self.ambient_channel = None
        self.tracks = {}
        self.sfx_map = {}
        self.settings = settings_manager
        
        # Default volumes
        self.volumes = {
            "master": 1.0,
            "music": 1.0,
            "sfx": 1.0
        }
        
        # Load volumes from settings if available
        if self.settings:
            self.volumes["master"] = self.settings.get("volume_master", 1.0)
            self.volumes["music"] = self.settings.get("volume_music", 1.0)
            self.volumes["sfx"] = self.settings.get("volume_sfx", 1.0)
        
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except Exception as e:
            logging.warning(f"SoundManager: Failed to initialize mixer. Silent mode enabled. Error: {e}")
            self.enabled = False

        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                self.tracks = data.get("tracks", {})
                self.sfx_map = data.get("sfx", {})
        except Exception as e:
            logging.error(f"SoundManager: Failed to load config {path}: {e}")

    def play_music(self, track_id, fade_ms=1000, loop=-1):
        if track_id == self.current_track:
            return

        self.current_track = track_id
        if not self.enabled:
            return

        file_path = self.tracks.get(track_id)
        if not file_path or not os.path.exists(file_path):
            logging.warning(f"SoundManager: Track '{track_id}' not found at {file_path}")
            return

        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self.volumes["music"] * self.volumes["master"])
            pygame.mixer.music.play(loops=loop, fade_ms=fade_ms)
        except Exception as e:
            logging.error(f"SoundManager: Error playing track '{track_id}': {e}")

    def stop_music(self, fade_ms=1000):
        if not self.enabled:
            return
        pygame.mixer.music.fadeout(fade_ms)
        self.current_track = None

    def play_sfx(self, sfx_id):
        if not self.enabled:
            return

        file_path = self.sfx_map.get(sfx_id)
        if not file_path or not os.path.exists(file_path):
            # Try to see if it's a direct path or if we should log
            if not file_path:
                logging.debug(f"SoundManager: SFX '{sfx_id}' not mapped.")
                return
            logging.warning(f"SoundManager: SFX file not found: {file_path}")
            return

        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(self.volumes["sfx"] * self.volumes["master"])
            sound.play()
        except Exception as e:
            logging.error(f"SoundManager: Error playing SFX '{sfx_id}': {e}")

    def on_signal(self, signal_type, payload=None):
        """Mapeia sinais do SignalBus para sons."""
        # Mapeamento básico por tipo de sinal
        if signal_type == "PICK_ITEM":
            item_name = payload.get("item", "").lower() if payload else ""
            if "gold" in item_name or "ouro" in item_name:
                self.play_sfx("coin")
            else:
                self.play_sfx("item_pickup")
        elif signal_type == "CHEST_OPENED":
            self.play_sfx("chest_open")
        elif signal_type == "LEVEL_UP":
            self.play_sfx("level_up")
        elif signal_type == "BATTLE_START":
            self.play_music("battle")
        elif signal_type == "BATTLE_END":
            # Retorna para a música do mapa? Precisamos de estado para isso.
            pass
        elif signal_type == "ANIM_TRIGGER":
            sfx_id = payload.get("sfx") if payload else None
            if sfx_id:
                self.play_sfx(sfx_id)

    def play_ambient(self, ambient_id, fade_ms=1000):
        if not self.enabled:
            return
            
        if ambient_id == self.current_ambient:
            return
            
        file_path = self.sfx_map.get(ambient_id)
        if not file_path or not os.path.exists(file_path):
            logging.warning(f"SoundManager: Ambient '{ambient_id}' not found.")
            return

        try:
            sound = pygame.mixer.Sound(file_path)
            if self.ambient_channel:
                self.ambient_channel.fadeout(fade_ms)
            
            self.ambient_channel = pygame.mixer.find_channel()
            if self.ambient_channel:
                self.ambient_channel.set_volume(self.volumes["sfx"] * self.volumes["master"])
                self.ambient_channel.play(sound, loops=-1, fade_ms=fade_ms)
                self.current_ambient = ambient_id
        except Exception as e:
            logging.error(f"SoundManager: Error playing ambient '{ambient_id}': {e}")

    def set_volume(self, group, value):
        clamped_value = max(0.0, min(1.0, value))
        self.volumes[group] = clamped_value
        
        # Persist to settings
        if self.settings:
            setting_key = f"volume_{group}"
            self.settings.set(setting_key, clamped_value, save=True)

        if self.enabled:
            if group == "music":
                pygame.mixer.music.set_volume(clamped_value * self.volumes["master"])
            elif group == "master":
                pygame.mixer.music.set_volume(self.volumes["music"] * clamped_value)

    def get_volume(self, group):
        return self.volumes.get(group, 0.0)
