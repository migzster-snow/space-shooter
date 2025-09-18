import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("fire laser!")

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

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

all_sprites = pygame.sprite.Group()

star_image = pygame.image.load(join("images", "star.png")).convert_alpha()
stars = []
for _ in range(20):
    star = Star(all_sprites, star_image)
    stars.append(star)
player = Player(all_sprites)

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

    all_sprites.update(delta_time)

    # draw the game
    display_surface.fill("darkgray")
    all_sprites.draw(display_surface)
    pygame.display.update()

# Uninitialise pygame
pygame.quit()
