import pytest
from src.core.particles import ParticleManager, Particle
from src.core.juice import JuiceService

class MockParticle(Particle):
    def __init__(self, x, y, lifetime):
        super().__init__(x, y, lifetime)
        self.updated = False

    def update(self, dt):
        super().update(dt)
        self.updated = True

def test_particle_manager_removes_dead_particles():
    manager = ParticleManager()
    p1 = MockParticle(0, 0, 1.0)
    p2 = MockParticle(10, 10, 0.5)
    
    manager.add(p1)
    manager.add(p2)
    
    assert len(manager.particles) == 2
    
    # Update by 0.6s -> p2 should die, p1 stays
    manager.update(0.6)
    assert len(manager.particles) == 1
    assert p1 in manager.particles
    assert p2 not in manager.particles
    assert p1.updated is True
    
    # Update by another 0.5s -> p1 should die
    manager.update(0.5)
    assert len(manager.particles) == 0

def test_particle_manager_emit_hit_creates_particles():
    manager = ParticleManager()
    manager.emit("hit", 5, 5, count=10)
    assert len(manager.particles) == 10

def test_particle_manager_emit_dust_creates_particles():
    manager = ParticleManager()
    manager.emit("dust", 5, 5, count=5)
    assert len(manager.particles) == 5

def test_juice_service_integration():
    manager = ParticleManager()
    juice = JuiceService(manager)
    
    juice.impact(100, 100)
    
    # Should have triggered particles
    assert len(manager.particles) > 0
    # Should have triggered camera shake/trauma
    assert juice.trauma > 0
    assert juice.flash_alpha > 0
