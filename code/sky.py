import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice

class Sky:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)
    
    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2*dt

        self.full_surf.fill(self.start_color)
        self.display_surf.blit(self.full_surf, (0,0), special_flags = pygame.BLEND_RGB_MULT)

class Drop(Generic):
    def __init__(self, pos, surf, groups, moving, z) -> None:
        #GENERAL SETUP
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        #MOVING
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)
    
    def update(self, dt):
        #MOVEMENT
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        #TIMER
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Rain:
    def __init__(self, all_sprites) -> None:
        self.all_sprites = all_sprites
        self.rain_drops = import_folder(RAIN_D_DIR)
        self.rain_floors = import_folder(RAIN_F_DIR)
        self.floor_w, self.floor_h = pygame.image.load(f'{WORLD_DIR}/ground.png').get_size()
    
    def create_floor(self):
        Drop(
            surf = choice(self.rain_floors),
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            moving = False,
            groups = self.all_sprites,
            z = LAYERS['rain floor'],
        )
    def create_drops(self): 
        Drop(
            surf = choice(self.rain_drops),
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            moving = True,
            groups = self.all_sprites,
            z = LAYERS['rain drops'],
        )
    def update(self):
        self.create_floor()
        self.create_drops()


