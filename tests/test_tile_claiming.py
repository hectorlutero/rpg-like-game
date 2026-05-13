import pytest
from src.models.world import World

class MockEntity:
    pass

def test_move_interactable_success():
    world = World([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    
    entity = MockEntity()
    world.add_interactable(0, 0, entity)
    
    # Act
    result = world.move_interactable(0, 0, 1, 0)
    
    # Assert
    assert result is True
    assert world.get_interactable_at(0, 0) is None
    assert world.get_interactable_at(1, 0) is entity

def test_move_interactable_collision_with_other_entity():
    world = World([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    
    entity1 = MockEntity()
    entity2 = MockEntity()
    world.add_interactable(0, 0, entity1)
    world.add_interactable(1, 0, entity2)
    
    # Act
    result = world.move_interactable(0, 0, 1, 0)
    
    # Assert
    assert result is False
    assert world.get_interactable_at(0, 0) is entity1
    assert world.get_interactable_at(1, 0) is entity2

def test_move_interactable_collision_with_wall():
    world = World([
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    
    entity = MockEntity()
    world.add_interactable(0, 0, entity)
    
    # Act
    result = world.move_interactable(0, 0, 1, 0)
    
    # Assert
    assert result is False
    assert world.get_interactable_at(0, 0) is entity

def test_move_interactable_out_of_bounds():
    world = World([
        [0, 0, 0]
    ])
    
    entity = MockEntity()
    world.add_interactable(0, 0, entity)
    
    # Act
    result = world.move_interactable(0, 0, -1, 0)
    
    # Assert
    assert result is False
    assert world.get_interactable_at(0, 0) is entity

def test_move_interactable_not_found():
    world = World([
        [0, 0, 0]
    ])
    
    # Act
    result = world.move_interactable(0, 0, 1, 0)
    
    # Assert
    assert result is False
