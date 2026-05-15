import random

class Particle:
    def __init__(self, x, y, lifetime, vx=0, vy=0, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.is_dead = False

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.is_dead = True

    def draw(self, screen):
        pass

class SparkParticle(Particle):
    def __init__(self, x, y, vx, vy, color=(255, 200, 50)):
        super().__init__(x, y, lifetime=random.uniform(0.2, 0.4), vx=vx, vy=vy, color=color)
        self.size = random.randint(1, 3)

    def draw(self, screen):
        import pygame
        # Simple line or pixel for spark
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class DustParticle(Particle):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, lifetime=random.uniform(0.5, 0.8), vx=vx, vy=vy, color=(200, 200, 200))
        self.size = random.randint(2, 4)

    def update(self, dt):
        super().update(dt)
        # Dust slows down and floats up
        self.vx *= 0.95
        self.vy -= 10 * dt # Gravity/Float

    def draw(self, screen):
        import pygame
        alpha = int((self.lifetime / self.max_lifetime) * 150)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

class ParticleManager:
    def __init__(self):
        self.particles = []

    def add(self, particle):
        self.particles.append(particle)

    def emit(self, p_type, x, y, count=1, **kwargs):
        for _ in range(count):
            if p_type == "hit":
                angle = random.uniform(0, 6.28)
                speed = random.uniform(50, 150)
                vx = random.uniform(-1, 1) * speed
                vy = random.uniform(-1, 1) * speed
                self.add(SparkParticle(x, y, vx, vy))
            elif p_type == "dust":
                vx = random.uniform(-20, 20)
                vy = random.uniform(-10, 10)
                self.add(DustParticle(x, y, vx, vy))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if not p.is_dead]

    def draw(self, screen):
        for p in sorted(self.particles, key=lambda p: p.y):
            p.draw(screen)
