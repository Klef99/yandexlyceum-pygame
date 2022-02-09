import os
import sys
import time

import pygame
from procgen import generate_dungeon
from random import randint


def load_image(name, colorkey=None):
    fullname = os.path.join('Assets/frames/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': {1: load_image('wall_left.png'), 2: load_image('wall_right.png'), 3: load_image('wall_mid.png')},
    'floors': {1: load_image('floor_1.png'), 2: load_image('floor_2.png'), 3: load_image('floor_3.png'),
              4: load_image('floor_4.png'), 5: load_image('floor_5.png'), 6: load_image('floor_6.png'),
              7: load_image('floor_7.png'), 8: load_image('floor_8.png')}
}


walls_textures = {'wall': {1: load_image('wall_left.png'), 2: load_image('wall_right.png'),
                           3: load_image('wall_mid.png')}}


lava_fountains_anims = {
    1: load_image('wall_fountain_mid_red_anim_f0.png'),
    2: load_image('wall_fountain_mid_red_anim_f1.png'),
    3: load_image('wall_fountain_mid_red_anim_f2.png')
}


lava_fountains_bottom_anims = {
    1: load_image('wall_fountain_basin_red_anim_f0.png'),
    2: load_image('wall_fountain_basin_red_anim_f1.png'),
    3: load_image('wall_fountain_basin_red_anim_f2.png')
}


player_anims = {
    'right': {1: load_image('knight_m_run_r_anim_f0.png'), 2: load_image('knight_m_run_r_anim_f1.png'),
              3: load_image('knight_m_run_r_anim_f2.png'), 4: load_image('knight_m_run_r_anim_f3.png')},
    'left': {1: load_image('knight_m_run_l_anim_f0.png'), 2: load_image('knight_m_run_l_anim_f1.png'),
             3: load_image('knight_m_run_l_anim_f2.png'), 4: load_image('knight_m_run_l_anim_f3.png')},
    'up': {1: load_image('knight_m_run_r_anim_f0.png'), 2: load_image('knight_m_run_r_anim_f1.png'),
           3: load_image('knight_m_run_r_anim_f2.png'), 4: load_image('knight_m_run_r_anim_f3.png')},
    'down': {1: load_image('knight_m_run_r_anim_f0.png'), 2: load_image('knight_m_run_r_anim_f1.png'),
             3: load_image('knight_m_run_r_anim_f2.png'), 4: load_image('knight_m_run_r_anim_f3.png')},
    'up_right': {1: load_image('knight_m_run_r_anim_f0.png'), 2: load_image('knight_m_run_r_anim_f1.png'),
                 3: load_image('knight_m_run_r_anim_f2.png'), 4: load_image('knight_m_run_r_anim_f3.png')},
    'right_down': {1: load_image('knight_m_run_r_anim_f0.png'), 2: load_image('knight_m_run_r_anim_f1.png'),
                   3: load_image('knight_m_run_r_anim_f2.png'), 4: load_image('knight_m_run_r_anim_f3.png')},
    'left_down': {1: load_image('knight_m_run_l_anim_f0.png'), 2: load_image('knight_m_run_l_anim_f1.png'),
                  3: load_image('knight_m_run_l_anim_f2.png'), 4: load_image('knight_m_run_l_anim_f3.png')},
    'up_left': {1: load_image('knight_m_run_l_anim_f0.png'), 2: load_image('knight_m_run_l_anim_f1.png'),
                3: load_image('knight_m_run_l_anim_f2.png'), 4: load_image('knight_m_run_l_anim_f3.png')},
    'stay_on_place': {1: load_image('knight_m_idle_anim_f0.png'), 2: load_image('knight_m_idle_anim_f1.png'),
                      3: load_image('knight_m_idle_anim_f2.png'), 4: load_image('knight_m_idle_anim_f3.png')}
}

tile_width = tile_height = 16
# основной персонаж
player = None
chests = []
enemies = []
doors = []
walls_inner_top_right = []
walls_inner_top_left = []
walls_side_mid_left = []
walls_side_mid_right = []
walls_corner_left = []
walls_corner_right = []
walls_top_left = []
walls_top_right = []
walls_top_mid = []
walls_side_front_left = []
walls_side_front_right = []
walls_side_top_left = []
walls_side_top_right = []
walls_inner_top_left_out = []
walls_top_mid_in = []
lava_fountains_mid = []
lava_fountains_bottom = []
lava_fountains_top = []


player_image = load_image('knight_m_run_r_anim_f0.png')
enemy_image = load_image('big_demon_idle_anim_f0.png')
chest_image = load_image('chest_empty_open_anim_f0.png')
door_image = load_image('doors_all3.png')
wall_inner_top_right_image = load_image('wall_inner_corner_l_top_rigth.png')
wall_inner_top_left_image = load_image('wall_inner_corner_l_top_left.png')
wall_side_mid_left_image = load_image('wall_side_mid_right.png')
wall_side_mid_right_image = load_image('wall_side_mid_left.png')
wall_corner_left_image = load_image('wall_corner_left.png')
wall_corner_right_image = load_image('wall_corner_right.png')
wall_top_left_image = load_image('wall_top_left.png')
wall_top_right_image = load_image('wall_top_right.png')
wall_top_mid_image = load_image('wall_top_mid.png')
wall_inner_top_left_out_image = load_image('wall_inner_corner_l_top_left.png')
wall_top_mid_in_image = load_image('wall_top_mid.png')
wall_side_front_left_image = load_image('wall_side_front_left.png')
wall_side_front_right_image = load_image('wall_side_front_right.png')
wall_side_top_left_image = load_image('wall_side_top_left.png')
wall_side_top_right_image = load_image('wall_side_top_right.png')
lava_fountain_top_image = load_image('wall_fountain_top.png')

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

wall_inner_top_right_group = pygame.sprite.Group()
wall_inner_top_left_group = pygame.sprite.Group()
wall_side_mid_left_group = pygame.sprite.Group()
wall_side_mid_right_group = pygame.sprite.Group()
wall_corner_left_group = pygame.sprite.Group()
wall_corner_right_group = pygame.sprite.Group()
wall_top_left_group = pygame.sprite.Group()
wall_top_right_group = pygame.sprite.Group()
wall_top_mid_group = pygame.sprite.Group()
wall_inner_top_left_out_group = pygame.sprite.Group()
wall_top_mid_in_group = pygame.sprite.Group()
wall_side_front_left_group = pygame.sprite.Group()
wall_side_front_right_group = pygame.sprite.Group()
wall_side_top_left_group = pygame.sprite.Group()
wall_side_top_right_group = pygame.sprite.Group()
wall_mid_group = pygame.sprite.Group()

lava_fountain_group = pygame.sprite.Group()
lava_fountain_bottom_group = pygame.sprite.Group()
lava_fountain_top_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ':':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
            elif level[y][x] == '#':
                Wall_mid(walls_textures['wall'][3], x, y)
            elif level[y][x] == 'L':
                Tile(tile_images['wall'][1], x, y)
            elif level[y][x] == 'R':
                Tile(tile_images['wall'][2], x, y)
            elif level[y][x] == '+':
                Tile(tile_images['floors'][randint(1, 2)], x, y)
                walls_inner_top_right.append(Wall_inner_top_right(x, y))
            elif level[y][x] == '-':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_inner_top_left.append(Wall_inner_top_left(x, y))
            elif level[y][x] == "'":
                walls_top_left.append(Wall_top_left(x, y))
            elif level[y][x] == '"':
                walls_top_right.append(Wall_top_right(x, y))
            elif level[y][x] == '0':
                walls_top_mid.append(Wall_top_mid(x, y))
            elif level[y][x] == '1':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_top_mid_in.append(Wall_top_mid_in(x, y))
            elif level[y][x] == '*':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_side_mid_left.append(Wall_side_mid_left(x, y))
            elif level[y][x] == '/':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_side_mid_right.append(Wall_side_mid_right(x, y))
            elif level[y][x] == '>':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_corner_left.append(Wall_corner_left(x, y))
            elif level[y][x] == '<':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_corner_right.append(Wall_corner_right(x, y))
            elif level[y][x] == '<':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_corner_right.append(Wall_corner_right(x, y))
            elif level[y][x] == '[':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_side_front_left.append(Wall_side_front_left(x, y))
            elif level[y][x] == ']':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_side_front_right.append(Wall_side_front_right(x, y))
            elif level[y][x] == '}':
                walls_inner_top_left_out.append(Wall_inner_top_left_out(x, y))
            elif level[y][x] == '@':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                enemies.append(Enemy(x, y))
            elif level[y][x] == '?':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                chests.append(Chest(x, y))
            elif level[y][x] == '=':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                doors.append(Door(x, y))
            elif level[y][x] == '(':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_side_top_left.append(Wall_side_top_left(x, y))
            elif level[y][x] == ')':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                walls_side_top_right.append(Wall_side_top_right(x, y))
            elif level[y][x] == 'F':
                lava_fountains_mid.append(Lava_fountains(x, y))
            elif level[y][x] == 'W':
                lava_fountains_bottom.append(Lava_fountains_bottom(x, y))
            elif level[y][x] == '^':
                Tile(tile_images['floors'][randint(1, 8)], x, y)
                lava_fountains_top.append(Lava_fountains_top(x, y))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Lava_fountains_top(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lava_fountain_top_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = lava_fountain_top_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Lava_fountains(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lava_fountain_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = lava_fountains_anims[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Lava_fountains_bottom(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lava_fountain_bottom_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = lava_fountains_bottom_anims[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_mid(pygame.sprite.Sprite):
    def __init__(self, im, pos_x, pos_y):
        super().__init__(wall_mid_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = im
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(chest_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = chest_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 5)


class Wall_side_top_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_top_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_side_top_left_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_top_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_top_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_side_top_right_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_mid_in(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_mid_in_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_top_mid_in_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_front_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_front_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_side_front_left_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_front_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_front_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_side_front_right_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_inner_top_left_out(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_inner_top_left_out_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_inner_top_left_out_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_top_left_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_mid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_mid_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_top_mid_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_top_right_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_corner_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_corner_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_corner_left_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_corner_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_corner_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_corner_right_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_inner_top_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_inner_top_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_inner_top_right_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_inner_top_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_inner_top_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_inner_top_left_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_mid_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_mid_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_side_mid_left_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_mid_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_mid_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_side_mid_right_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = door_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 18, tile_height * pos_y - 19)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 20)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 20
        )
        self.healt_init()

    def healt_init(self):
        self.current_health = 500
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self):
        self.health()

    def health(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(5, 10, health_bar_width, 15)
        transition_bar = pygame.Rect(health_bar.right, 10, transition_width, 15)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)
        pygame.draw.rect(screen, transition_color, transition_bar)
        pygame.draw.rect(screen, (255, 255, 255), (5, 10, self.health_bar_length, 15), 4)

    def can_player_move1(self, key):
        if key == pygame.K_a:
            if not self.checker_wall_for_left():
                self.image = player_anims['left'][1]
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['left'][2]
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['left'][3]
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['left'][4]
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

        elif key == pygame.K_d:
            if not self.checker_wall_for_right():
                self.image = player_anims['right'][1]
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['right'][2]
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['right'][3]
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['right'][4]
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

        elif key == pygame.K_w:
            if not self.checker_wall_for_top():
                self.image = player_anims['up'][1]
                self.rect.y -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up'][2]
                self.rect.y -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up'][3]
                self.rect.y -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up'][4]
                self.rect.y -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

        elif key == pygame.K_s:
            if not self.checker_wall_for_bottom():
                self.image = player_anims['down'][1]
                self.rect.y += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['down'][2]
                self.rect.y += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['down'][3]
                self.rect.y += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['down'][4]
                self.rect.y += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

    def checker_wall_for_left(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_left_group):
            return True
        elif pygame.sprite.spritecollideany(self, wall_inner_top_left_group):
            return True
        else:
            self.rect = self.rect.move(-1, 0)
            return False

    def checker_wall_for_right(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        else:
            self.rect = self.rect.move(1, 0)
            return False

    def checker_wall_for_top(self):
        global flagD, flagU, flagL, flagR
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        if pygame.sprite.spritecollideany(self, wall_top_mid_in_group):
            flagR = flagL = flagU = flagD = False
            return True
        else:
            self.rect = self.rect.move(0, -1)
            return False

    def checker_wall_for_bottom(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        else:
            self.rect = self.rect.move(0, 1)
            return False

    def can_player_move2(self, key1, key2):
        if (key1 == pygame.K_d and key2 == pygame.K_w) or (key1 == pygame.K_w and key2 == pygame.K_d):
            if not self.checker_wall_for_up_right():
                self.image = player_anims['up_right'][1]
                self.rect.y -= 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up_right'][2]
                self.rect.y -= 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up_right'][3]
                self.rect.y -= 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up_right'][4]
                self.rect.y -= 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

        elif (key1 == pygame.K_d and key2 == pygame.K_s) or (key1 == pygame.K_s and key2 == pygame.K_d):
            if not self.checker_wall_for_right_down():
                self.image = player_anims['right_down'][1]
                self.rect.y += 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['right_down'][2]
                self.rect.y += 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['right_down'][3]
                self.rect.y += 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['right_down'][4]
                self.rect.y += 2
                self.rect.x += 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

        elif (key1 == pygame.K_a and key2 == pygame.K_s) or (key1 == pygame.K_s and key2 == pygame.K_a):
            if not self.checker_wall_for_left_down():
                self.image = player_anims['left_down'][1]
                self.rect.y += 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['left_down'][2]
                self.rect.y += 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['left_down'][3]
                self.rect.y += 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['left_down'][4]
                self.rect.y += 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

        elif (key1 == pygame.K_a and key2 == pygame.K_w) or (key1 == pygame.K_w and key2 == pygame.K_a):
            if not self.checker_wall_for_up_left():
                self.image = player_anims['up_left'][1]
                self.rect.y -= 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up_left'][2]
                self.rect.y -= 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up_left'][3]
                self.rect.y -= 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

                self.image = player_anims['up_left'][4]
                self.rect.y -= 2
                self.rect.x -= 2
                all_sprites.draw(screen)
                player_group.draw(screen)
                player_group.update()
                all_sprites.update()
                pygame.display.flip()
                time.sleep(0.05)

    def checker_wall_for_up_right(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        else:
            self.rect = self.rect.move(1, -1)
            return False

    def checker_wall_for_right_down(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        else:
            self.rect = self.rect.move(1, 1)
            return False

    def checker_wall_for_left_down(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        else:
            self.rect = self.rect.move(-1, 1)
            return False

    def checker_wall_for_up_left(self):
        if pygame.sprite.spritecollideany(self, wall_side_mid_right_group):
            return True
        else:
            self.rect = self.rect.move(-1, -1)
            return False

    def stay_on_place(self):
        self.image = player_anims['stay_on_place'][1]
        all_sprites.draw(screen)
        player_group.draw(screen)
        player_group.update()
        all_sprites.update()
        pygame.display.flip()
        time.sleep(0.05)

        self.image = player_anims['stay_on_place'][2]
        all_sprites.draw(screen)
        player_group.draw(screen)
        player_group.update()
        all_sprites.update()
        pygame.display.flip()
        time.sleep(0.05)

        self.image = player_anims['stay_on_place'][3]
        all_sprites.draw(screen)
        player_group.draw(screen)
        player_group.update()
        all_sprites.update()
        pygame.display.flip()
        time.sleep(0.05)

        self.image = player_anims['stay_on_place'][4]
        all_sprites.draw(screen)
        player_group.draw(screen)
        player_group.update()
        all_sprites.update()
        pygame.display.flip()
        time.sleep(0.05)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Deep Dark Dungeon (DDD)')
    generate_dungeon('map.txt', 70, 40, 110, 50, 60)
    level = load_level('example_map2.txt')
    player, level_x, level_y = generate_level(level)
    size = width, height = level_x * tile_width, level_y * tile_height
    screen = pygame.display.set_mode(size)
    running = True
    flagR = flagL = flagD = flagU = False
    see_L = True
    see_R = see_U = see_D = False
    fps = 60
    clock = pygame.time.Clock()
    pygame.mixer.music.load('Assets/Sounds/music_on_the_background.mp3')
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    flagL = True
                if event.key == pygame.K_w:
                    flagU = True
                if event.key == pygame.K_s:
                    flagD = True
                if event.key == pygame.K_d:
                    flagR = True
                if event.key == pygame.K_UP:
                    player.get_health(200)
                    pygame.mixer.music.load('Assets/Sounds/Health_player.mp3')
                    pygame.mixer.music.play()
                if event.key == pygame.K_DOWN:
                    player.get_damage(200)
                    pygame.mixer.music.load('Assets/Sounds/Damage_player.mp3')
                    pygame.mixer.music.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    flagL = False
                if event.key == pygame.K_d:
                    flagR = False
                if event.key == pygame.K_w:
                    flagU = False
                if event.key == pygame.K_s:
                    flagD = False

        if flagR and flagU:
            player.can_player_move2(pygame.K_d, pygame.K_w)
        elif flagR and flagD:
            player.can_player_move2(pygame.K_d, pygame.K_s)
        elif flagL and flagD:
            player.can_player_move2(pygame.K_a, pygame.K_s)
        elif flagU and flagL:
            player.can_player_move2(pygame.K_a, pygame.K_w)
        elif flagR:
            player.can_player_move1(pygame.K_d)
        elif flagL:
            player.can_player_move1(pygame.K_a)
        elif flagU:
            player.can_player_move1(pygame.K_w)
        elif flagD:
            player.can_player_move1(pygame.K_s)
        else:
            player.stay_on_place()
        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        chest_group.draw(screen)
        door_group.draw(screen)
        wall_inner_top_right_group.draw(screen)
        wall_inner_top_left_group.draw(screen)
        wall_side_mid_left_group.draw(screen)
        wall_side_mid_right_group.draw(screen)
        wall_corner_left_group.draw(screen)
        wall_corner_right_group.draw(screen)
        wall_top_left_group.draw(screen)
        wall_top_right_group.draw(screen)
        wall_top_mid_group.draw(screen)
        wall_inner_top_left_out_group.draw(screen)
        wall_top_mid_in_group.draw(screen)
        wall_side_front_left_group.draw(screen)
        wall_side_front_right_group.draw(screen)
        wall_side_top_left_group.draw(screen)
        wall_side_top_right_group.draw(screen)
        lava_fountain_group.draw(screen)
        lava_fountain_bottom_group.draw(screen)
        lava_fountain_top_group.draw(screen)


        all_sprites.update()
        tiles_group.update()
        player_group.update()
        door_group.update()
        chest_group.update()
        enemy_group.update()
        wall_inner_top_right_group.update()
        wall_inner_top_left_group.update()
        wall_side_mid_left_group.update()
        wall_side_mid_right_group.update()
        wall_corner_left_group.update()
        wall_corner_right_group.update()
        wall_top_left_group.update()
        wall_top_right_group.update()
        wall_top_mid_group.update()
        wall_inner_top_left_out_group.update()
        wall_top_mid_in_group.update()
        wall_side_front_left_group.update()
        wall_side_front_right_group.update()
        wall_side_top_left_group.update()
        wall_side_top_right_group.update()
        lava_fountain_group.update()
        lava_fountain_bottom_group.update()
        lava_fountain_top_group.update()

        pygame.display.flip()
    pygame.quit()
