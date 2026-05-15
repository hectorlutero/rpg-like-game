from src.models.world import Position

class AnimationMixin:
    """Mixin to provide standard sprite animation state and logic."""
    def init_animation(self, sheet_id, state="idle"):
        self.sprite_sheet_id = sheet_id
        self.state = state
        self.frame_index = 0
        self.animation_timer = 0

    def update_animation(self, dt):
        from src.core.assets import AssetManager
        am = AssetManager()
        
        # Get facing_direction if it exists, else use state as is
        facing = getattr(self, "facing_direction", None)
        anim_id = f"{self.state}_{facing}" if facing else self.state
        
        duration = am.get_animation_duration(self.sprite_sheet_id, anim_id)
        frames = am.get_animation(self.sprite_sheet_id, anim_id)
        
        if len(frames) > 0:
            self.animation_timer += dt
            if self.animation_timer >= duration:
                advancement = self.animation_timer // duration
                self.frame_index = (self.frame_index + advancement) % len(frames)
                self.animation_timer = self.animation_timer % duration
        else:
            self.frame_index = 0
            self.animation_timer = 0
