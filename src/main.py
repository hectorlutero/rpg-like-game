import pygame
import sys
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World

def main():
    # Initialize Pygame
    pygame.init()
    
    # Screen settings
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("RPG Classic - Pygame")
    
    clock = pygame.time.Clock()
    
    # Simple map grid (0 = walkable, 1 = solid)
    # 25x19 grid for 32x32 tiles (800/32=25, 600/32=18.75)
    map_grid = [[0 for _ in range(25)] for _ in range(20)]
    # Add some walls
    for i in range(25):
        map_grid[0][i] = 1
        map_grid[19][i] = 1
    for i in range(20):
        map_grid[i][0] = 1
        map_grid[i][24] = 1
        
    world = World(map_grid, tile_size=32)
    
    # Initialize Player
    player = Character("Herói", Warrior())
    player.position.x = 64
    player.position.y = 64
    player_speed = 4
    
    # Game Loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0 # Delta time in seconds
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 2. Input Handling (Movement)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = player_speed
            
        # 3. Collision & Movement
        if dx != 0 or dy != 0:
            new_x = player.position.x + dx
            new_y = player.position.y + dy
            
            # Simple collision check for the player center point
            if world.can_move_to(player, new_x, new_y):
                player.position.move(dx, dy)
        
        # 4. Drawing
        screen.fill((30, 30, 30)) # Dark background
        
        # Draw Map
        for y, row in enumerate(world.grid):
            for x, tile in enumerate(row):
                if tile == 1: # Wall
                    pygame.draw.rect(screen, (100, 100, 100), (x*32, y*32, 32, 32))
                else: # Floor
                    pygame.draw.rect(screen, (50, 50, 50), (x*32, y*32, 32, 32), 1)
        
        # Draw Player (simple blue square)
        pygame.draw.rect(screen, (0, 100, 255), (player.position.x - 16, player.position.y - 16, 32, 32))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
