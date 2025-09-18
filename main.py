import pygame
from os.path import join
from random import randint

# Initialise pygame
pygame.init()

# Set up the screen
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the screen
pygame.display.set_caption("Space Shooter")

# Run the main loop
running = True

# Set up the clock
clock = pygame.time.Clock()

# Set up a plain surface
surface = pygame.Surface((100, 200))
surface.fill("orange")
x = 100

# Set up a surface with an image
player_surface = pygame.image.load(join("images", "player.png")).convert_alpha()
player_rectangle = player_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2()
player_speed = 300

star_surface = pygame.image.load(join("images", "star.png")).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_rectangle = meteor_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_rectangle = laser_surface.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

# Main loop
while running:
    delta_time = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction
    player_rectangle.center += player_direction * player_speed * delta_time

    # draw the game
    display_surface.fill("darkgray")
    for star_position in star_positions:
        display_surface.blit(star_surface, star_position)
    display_surface.blit(meteor_surface, meteor_rectangle)
    display_surface.blit(laser_surface, laser_rectangle)
    display_surface.blit(player_surface, player_rectangle)
    pygame.display.update()

# Uninitialise pygame
pygame.quit()
