import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True 

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_image, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, image, position):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(midbottom=position)
        self.speed = 400

    def update(self, delta_time):
        self.rect.centery -= self.speed * delta_time
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, image, position):
        super().__init__(groups)
        self.original_image = image
        self.image = image
        self.rect = self.image.get_frect(center=position)
        self.speed = 400
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0

    def update(self, delta_time):
        self.rotation += self.rotation_speed * delta_time
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.rect.center += self.direction.normalize() * self.speed * delta_time
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, position, frames):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0 
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=position)
        self.animation_speed = 20

    def update(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
        

def collision():
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(all_sprites, laser.rect.midtop, explosion_frames)

def display_score():
    current_time = pygame.time.get_ticks()
    text_surface = font.render(str(current_time), True, (240, 240, 240))
    text_rectangle = text_surface.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surface, text_rectangle)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rectangle.inflate(20, 10).move(0, -5), 5, 10)


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
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

star_image = pygame.image.load(join("images", "star.png")).convert_alpha()
laser_image = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_image = pygame.image.load(join("images", "meteor.png")).convert_alpha()
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 40)
explosion_frames = [pygame.image.load(join("images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]


stars = []
for _ in range(20):
    star = Star(all_sprites, star_image)
    stars.append(star)
player = Player(all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# Main loop
while running:
    delta_time = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_sprites), meteor_image, (randint(0, WINDOW_WIDTH), randint(-200, -100))) 

    all_sprites.update(delta_time)

    collision()

    # draw the game
    display_surface.fill("#3a2e3f")
    all_sprites.draw(display_surface)
    display_score()

    pygame.display.update()

# Uninitialise pygame
pygame.quit()
