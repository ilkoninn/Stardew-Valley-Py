import pygame
from settings import *

class Overlay:
    def __init__(self, player) -> None:
        #GENERAL SETUP
        self.display_surf = pygame.display.get_surface()
        self.player = player

        #IMPORTANTS
        overlay_path = OVERLAY_DIR
        self.tools_surf = {tool:pygame.image.load(f'{overlay_path}/{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed:pygame.image.load(f'{overlay_path}/{seed}.png').convert_alpha() for seed in player.seeds}
        print(OVERLAY_DIR)
        print(self.tools_surf)
        print(self.seeds_surf)

    def display(self):
        #TOOL
        tools_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tools_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surf.blit(tools_surf, tool_rect)

        #SEEDS
        seeds_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seeds_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surf.blit(seeds_surf, seed_rect) 


