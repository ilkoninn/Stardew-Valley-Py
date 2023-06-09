import pygame
from settings import *
from player import Player
from overlay import Overlay
from transition import Transition
from sprites import (
        Generic, Water, 
        WildFlower, Tree, 
        Interaction, Particle
    )
from pytmx.util_pygame import load_pygame
from support import *
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu

class Level:
    def __init__(self) -> None:

        #GET THE DISPLAY SURFACE
        self.display_surf = pygame.display.get_surface()

        #SPRITE GROUPS
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group() 

        self.soil_layer = SoilLayer(self.all_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        #SKY
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0,10) > 7
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        #SHOP
        self.menu = Menu(
            player = self.player,
            toggle_menu = self.toggle_shop,
        )
        self.shop_active = False

        # MUSIC
        self.success = pygame.mixer.Sound(f'{AUDIO_DIR}/success.wav')
        self.success.set_volume(0.3)

        self.music = pygame.mixer.Sound(f'{AUDIO_DIR}/music.mp3')
        self.music.play(loops = -1)

    def setup(self):
        tmx_data = load_pygame(f'{DATA_DIR}/map.tmx')

        #HOUSE
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE), 
                    surf= surf, 
                    groups = self.all_sprites, 
                    z= LAYERS['house bottom']
                )

        
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE), 
                    surf= surf, 
                    groups = self.all_sprites,
                )
        
        #FANCE
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE), 
                surf= surf, 
                groups = self.all_sprites,
            ) 
        
        #WATER
        water_path = WATER_DIR
        water_frames = import_folder(water_path)
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water(
                pos = (x * TILE_SIZE, y * TILE_SIZE), 
                frames = water_frames, 
                groups = [self.all_sprites, self.collision_sprites],
            ) 

        #TREES
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos = (obj.x, obj.y), 
                surf = obj.image, 
                groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
                name = obj.name,
                player_add = self.player_add,
            ) 
     
        #WIDLFLOWERS
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(
                pos = (obj.x, obj.y), 
                surf = obj.image, 
                groups = self.all_sprites,
            ) 
        #PLAYER
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    group = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites,
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    toggle_shop = self.toggle_shop
                ) 
            if obj.name == 'Bed':
                Interaction(
                    pos = (obj.x, obj.y),
                    size = (obj.width, obj.height),
                    groups = self.interaction_sprites,
                    name = obj.name,
                )
            
            if obj.name == 'Trader':
                Interaction(
                    pos = (obj.x, obj.y),
                    size = (obj.width, obj.height),
                    groups = self.interaction_sprites,
                    name = obj.name,
                )

        #COLLISON TILES
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE), 
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                groups= self.collision_sprites,
            )


        Generic(
            pos = (0, 0), 
            surf = pygame.image.load(f'{WORLD_DIR}/ground.png').convert_alpha(), 
            groups=self.all_sprites,
            z = LAYERS['ground'],
        )

    def reset(self):
        #PLANTS
        self.soil_layer.update_plants()


        #SOIL RESET
        self.soil_layer.remove_water()

        #RANDOMIZE THE RAIN
        self.raining = randint(0,10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        #RESET EVERYTHING
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

        #SKY 
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def run(self, dt):
        #DRAWING LOGIC
        self.display_surf.fill('black')
        self.all_sprites.custom_draw(self.player)
        
        #UPDATES
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()
        
        #WEATHER
        self.overlay.display()
        
        if self.raining and not self.shop_active:
            self.rain.update() 
        
        self.sky.display(dt)

        #TRANSITION OVERLAY 
        if self.player.sleep:
            self.transition.play()
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surf.blit(sprite.image, offset_rect)
                
                    #ANALYTICS OF POSITION
                    # if sprite == player:
                    #     pygame.draw.rect(self.display_surf, 'red', offset_rect, 5)
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surf, 'green', hitbox_rect, 5)
                    #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                    #     pygame.draw.circle(self.display_surf, 'blue', target_pos, 5)

    

