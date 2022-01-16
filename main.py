import os
import sys

import pygame
from procgen import generate_dungeon
from tiles import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Deep Dark Dungeon (DDD)')
    generate_dungeon('map.txt', 40, 30, 110, 50, 60)
    player, level_x, level_y = generate_level(load_level('map.txt'))
    size = width, height = level_x * tile_width, level_y * tile_height
    screen = pygame.display.set_mode(size)
    running = True
    x_pos = 0
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
