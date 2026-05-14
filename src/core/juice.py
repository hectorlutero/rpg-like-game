import random

class JuiceService:
    def __init__(self):
        self.trauma = 0.0
        self.flash_alpha = 0
        self.flash_color = (255, 255, 255)
        self.hit_stop_time = 0.0
        self.camera_offset = [0, 0]

    def shake(self, amount):
        self.trauma = min(1.0, self.trauma + amount)

    def flash(self, color=(255, 255, 255), duration_alpha=255):
        self.flash_color = color
        self.flash_alpha = duration_alpha

    def hit_stop(self, duration):
        self.hit_stop_time = max(self.hit_stop_time, duration)

    def is_hit_stopping(self):
        return self.hit_stop_time > 0

    def update(self, dt):
        # Shake Decay
        if self.trauma > 0:
            self.trauma = max(0, self.trauma - dt * 1.5)
            shake_amount = (self.trauma ** 2) * 15
            self.camera_offset[0] = random.uniform(-shake_amount, shake_amount)
            self.camera_offset[1] = random.uniform(-shake_amount, shake_amount)
        else:
            self.camera_offset = [0, 0]

        # Flash Decay
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - dt * 800)

        # Hit Stop Decay
        if self.hit_stop_time > 0:
            self.hit_stop_time -= dt
            if self.hit_stop_time < 0:
                self.hit_stop_time = 0.0
