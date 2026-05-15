import json
import os
import pygame

class MetadataLoader:
    def load(self, path: str) -> dict:
        if not os.path.exists(path):
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

class AssetManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._sheets = {}
        self._sprite_cache = {}
        self._loader = MetadataLoader()
        self._placeholder = self._create_placeholder()
        self._initialized = True

    def _create_placeholder(self):
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255)) # Magenta placeholder
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, 16, 16))
        pygame.draw.rect(surf, (0, 0, 0), (16, 16, 16, 16))
        return surf

    def register_sheet(self, sheet_id: str, image_path: str, meta_path: str):
        """Registers a SpriteSheet and its metadata for lazy loading."""
        self._sheets[sheet_id] = {
            "image_path": image_path,
            "meta_path": meta_path,
            "surface": None,
            "metadata": None
        }

    def _ensure_sheet_loaded(self, sheet_id: str):
        if sheet_id not in self._sheets:
            return False
        
        sheet = self._sheets[sheet_id]
        if sheet["surface"] is None:
            try:
                sheet["surface"] = pygame.image.load(sheet["image_path"]).convert_alpha()
            except (pygame.error, FileNotFoundError):
                sheet["surface"] = self._placeholder
                
        if sheet["metadata"] is None:
            sheet["metadata"] = self._loader.load(sheet["meta_path"])
            
        return True

    def get_sprite(self, sheet_id: str, sprite_id: str) -> pygame.Surface:
        """Lazily slices and returns a sprite from the specified sheet."""
        cache_key = f"{sheet_id}:{sprite_id}"
        if cache_key in self._sprite_cache:
            return self._sprite_cache[cache_key]
        
        if not self._ensure_sheet_loaded(sheet_id):
            return self._placeholder
            
        sheet = self._sheets[sheet_id]
        metadata = sheet["metadata"]
        
        if not metadata or "sprites" not in metadata or sprite_id not in metadata["sprites"]:
            return self._placeholder
            
        data = metadata["sprites"][sprite_id]
        rect = pygame.Rect(data["x"], data["y"], data["w"], data["h"])
        
        # Slicing
        sprite = pygame.Surface(rect.size, pygame.SRCALPHA)
        sprite.blit(sheet["surface"], (0, 0), rect)
        
        self._sprite_cache[cache_key] = sprite
        return sprite

    def get_hitbox_data(self, sheet_id: str, sprite_id: str) -> list:
        """Returns [offset_x, offset_y, w, h] for a given sprite, or defaults."""
        if not self._ensure_sheet_loaded(sheet_id):
            return [0, 16, 32, 16] # Default: bottom half
            
        sheet = self._sheets[sheet_id]
        metadata = sheet["metadata"]
        
        if not metadata or "sprites" not in metadata or sprite_id not in metadata["sprites"]:
            return [0, 16, 32, 16]
            
        data = metadata["sprites"][sprite_id]
        return data.get("hitbox", [0, 16, 32, 16])

    def get_sprite_size(self, sheet_id: str, sprite_id: str) -> tuple:
        """Returns (w, h) for a given sprite, or (32, 32) if not found."""
        if not self._ensure_sheet_loaded(sheet_id):
            return (32, 32)
            
        sheet = self._sheets[sheet_id]
        metadata = sheet["metadata"]
        
        if not metadata or "sprites" not in metadata or sprite_id not in metadata["sprites"]:
            return (32, 32)
            
        data = metadata["sprites"][sprite_id]
        return (data.get("w", 32), data.get("h", 32))

    def get_animation(self, sheet_id: str, anim_id: str) -> list:
        """Returns a list of frames for a given animation ID."""
        if not self._ensure_sheet_loaded(sheet_id):
            return [self._placeholder]
            
        sheet = self._sheets[sheet_id]
        metadata = sheet["metadata"]
        
        if not metadata or "animations" not in metadata or anim_id not in metadata["animations"]:
            return [self._placeholder]
            
        frame_ids = metadata["animations"][anim_id]
        return [self.get_sprite(sheet_id, fid) for fid in frame_ids]

    def get_animation_duration(self, sheet_id: str, anim_id: str) -> int:
        """Returns the frame duration for an animation in ms, defaults to 100."""
        if not self._ensure_sheet_loaded(sheet_id):
            return 100
            
        sheet = self._sheets[sheet_id]
        metadata = sheet["metadata"]
        
        if not metadata or "animations" not in metadata:
            return 100
            
        # Try to find specific duration in metadata, else default
        duration_key = f"{anim_id}_duration"
        return metadata["animations"].get(duration_key, 100)
