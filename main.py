import os
import sys
import time

import pygame
from procgen import generate_dungeon
from random import randint

defeat_enemy = 0


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


def get_best_score(score):
    with open('score.txt') as file:
        best_score = int(file.readlines()[-1])
    if best_score <= score:
        best_score = score
        with open('score.txt', 'w') as file:
            file.write(str(best_score))
    return best_score


floor_textures = {
    1: load_image('floor_1.png'),
    2: load_image('floor_2.png'),
    3: load_image('floor_3.png'),
    4: load_image('floor_4.png'),
    5: load_image('floor_5.png'),
    6: load_image('floor_6.png'),
    7: load_image('floor_7.png'),
    8: load_image('floor_8.png')
}

wall_textures = {'wall_front_mid': {1: load_image('wall_hole_1.png'),
                                    2: load_image('wall_hole_2.png'),
                                    3: load_image('wall_mid.png')},
                 'wall_front_left': load_image('wall_left.png'),
                 'wall_front_right': load_image('wall_right.png'),
                 'wall_inner_top_right_image': load_image('wall_inner_corner_l_top_rigth.png'),
                 'wall_inner_top_left_image': load_image('wall_inner_corner_l_top_left.png'),
                 'wall_side_mid_left_image': load_image('wall_side_mid_right4.png'),
                 'wall_side_mid_right_image': load_image('wall_side_mid_left4.png'),
                 'wall_corner_left_image': load_image('wall_corner_left.png'),
                 'wall_corner_right_image': load_image('wall_corner_right.png'),
                 'wall_top_left_image': load_image('wall_top_left.png'),
                 'wall_top_right_image': load_image('wall_top_right.png'),
                 'wall_top_mid_image': load_image('wall_top_mid.png'),
                 'wall_inner_top_left_out_image': load_image('wall_inner_corner_l_top_left.png'),
                 'wall_top_mid_in_image': load_image('wall_top_mid2.png'),
                 'wall_side_front_left_image': load_image('wall_side_front_left.png'),
                 'wall_side_front_right_image': load_image('wall_side_front_right.png'),
                 'wall_side_top_left_image': load_image('wall_side_top_left.png'),
                 'wall_side_top_right_image': load_image('wall_side_top_right.png'),
                 }

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
    'default': load_image('knight_m_run_r_anim_f0.png'),
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
empties = []


enemy_image = load_image('chort_idle_anim_f0.png')
chest_image = load_image('chest_empty_open_anim_f0.png')
chest_open_image = load_image('chest_full_open_anim_f2.png')
door_image = load_image('doors_all3.png')
door_open_image = load_image('doors_open.png')
lava_fountain_top_image = load_image('wall_fountain_top.png')
sword = load_image('weapon_anime_sword.png')
empty_image = load_image('empty.png')
shadow_checker_image = load_image('border_checker4.png')
border_floor_top_image = load_image('border_floor_t2.png')
border_floor_right_image = load_image('border_floor_r2.png')
border_floor_bottom_image = load_image('border_floor_b2.png')
border_floor_left_image = load_image('border_floor_l2.png')

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
wall_front_left_group = pygame.sprite.Group()
wall_front_right_group = pygame.sprite.Group()
wall_front_mid_group = pygame.sprite.Group()
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
lava_fountain_group = pygame.sprite.Group()
lava_fountain_bottom_group = pygame.sprite.Group()
lava_fountain_top_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
empty_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
shadow_checker_group = pygame.sprite.Group()
border_floor_top_group = pygame.sprite.Group()
border_floor_right_group = pygame.sprite.Group()
border_floor_bottom_group = pygame.sprite.Group()
border_floor_left_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y, weapon, shadow = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ':':
                Floor(x, y)
            elif level[y][x] == '#':
                Wall_front_mid(x, y)
                Border_floor_top(x, y)
                Border_floor_bottom(x, y)
            elif level[y][x] == 'L':
                Wall_front_left(x, y)
                Border_floor_bottom(x, y)
            elif level[y][x] == 'R':
                Wall_front_right(x, y)
                Border_floor_bottom(x, y)
            elif level[y][x] == '+':
                Floor(x, y)
                walls_inner_top_right.append(Wall_inner_top_right(x, y))
                Border_floor_right(x, y)
            elif level[y][x] == '-':
                Floor(x, y)
                walls_inner_top_left.append(Wall_inner_top_left(x, y))
                Border_floor_left(x, y)
            elif level[y][x] == "'":
                walls_top_left.append(Wall_top_left(x, y))
            elif level[y][x] == '"':
                walls_top_right.append(Wall_top_right(x, y))
            elif level[y][x] == '0':
                walls_top_mid.append(Wall_top_mid(x, y))
            elif level[y][x] == '1':
                Floor(x, y)
                walls_top_mid_in.append(Wall_top_mid_in(x, y))
            elif level[y][x] == '*':
                Floor(x, y)
                walls_side_mid_left.append(Wall_side_mid_left(x, y))
                Border_floor_left(x, y)
            elif level[y][x] == '/':
                Floor(x, y)
                walls_side_mid_right.append(Wall_side_mid_right(x, y))
                Border_floor_right(x, y)
            elif level[y][x] == '>':
                Floor(x, y)
                walls_corner_left.append(Wall_corner_left(x, y))
                Border_floor_top(x, y)
            elif level[y][x] == '<':
                Floor(x, y)
                walls_corner_right.append(Wall_corner_right(x, y))
                Border_floor_top(x, y)
            elif level[y][x] == '[':
                Floor(x, y)
                walls_side_front_left.append(Wall_side_front_left(x, y))
                Border_floor_right(x, y)
            elif level[y][x] == ']':
                Floor(x, y)
                walls_side_front_right.append(Wall_side_front_right(x, y))
                Border_floor_left(x, y)
            elif level[y][x] == '@':
                Floor(x, y)
                shadow = Shadow_checker(x, y)
                new_player = Player(x, y)
                weapon = Weapon(x, y)
            elif level[y][x] == '!':
                Floor(x, y)
                enemy = Enemy(x, y)
                enemies.append(enemy)
            elif level[y][x] == '?':
                Floor(x, y)
                chests.append(Chest(x, y))
            elif level[y][x] == '=':
                Floor(x, y)
                doors.append(Door(x, y))
            elif level[y][x] == '(':
                Floor(x, y)
                walls_side_top_left.append(Wall_side_top_left(x, y))
            elif level[y][x] == ')':
                Floor(x, y)
                walls_side_top_right.append(Wall_side_top_right(x, y))
            elif level[y][x] == 'F':
                lava_fountains_mid.append(Lava_fountains(x, y))
            elif level[y][x] == 'W':
                lava_fountains_bottom.append(Lava_fountains_bottom(x, y))
            elif level[y][x] == '^':
                Floor(x, y)
                lava_fountains_top.append(Lava_fountains_top(x, y))
            elif level[y][x] == '_':
                empties.append(Empty(x, y))
            elif level[y][x] == '~':
                Floor(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, weapon, shadow


class Wall_front_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_front_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_front_left']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_front_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_front_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_front_right']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(floor_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = floor_textures[randint(1, 8)]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Empty(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(empty_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = empty_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


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


class Wall_front_mid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_front_mid_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_front_mid'][randint(1, 3)]
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
        self.notop = True

    def update(self):
        if (abs(player.rect.x - self.rect.x) <= 2 or abs(player.rect.y - self.rect.y) <= 2) and self.notop:
            self.notop = False
            self.image = chest_open_image
            player.score += 100


class Wall_side_top_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_top_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_side_top_left_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_top_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_top_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_side_top_right_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_mid_in(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_mid_in_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_top_mid_in_image']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 10)


class Wall_side_front_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_front_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_side_front_left_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_front_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_front_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_side_front_right_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_inner_top_left_out(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_inner_top_left_out_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_inner_top_left_out_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_top_left_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_mid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_mid_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_top_mid_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_top_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_top_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_top_right_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_corner_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_corner_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_corner_left_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_corner_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_corner_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_corner_right_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_inner_top_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_inner_top_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_inner_top_right_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_inner_top_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_inner_top_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_inner_top_left_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_mid_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_mid_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_side_mid_left_image']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall_side_mid_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_side_mid_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = wall_textures['wall_side_mid_right_image']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y)


class Border_floor_top(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(border_floor_top_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = border_floor_top_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 13)


class Border_floor_right(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(border_floor_right_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = border_floor_right_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y)


class Border_floor_bottom(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(border_floor_bottom_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = border_floor_bottom_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 7)


class Border_floor_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(border_floor_left_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = border_floor_left_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 3, tile_height * pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = door_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 18, tile_height * pos_y - 19)

    def open_door(self):
        self.image = door_open_image


class Shadow_checker(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(shadow_checker_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = shadow_checker_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 1, tile_height * pos_y + 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = enemy_image
        self.lives = 3
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 13)

    def taking_damage(self):
        global defeat_enemy
        self.lives -= 1
        if self.lives == 0:
            print('dead')
            defeat_enemy += 1
            player.score += 50
            self.image = floor_textures[3]

    def update(self):
        # if self.lives != 0:
        #     if abs(player.rect.x - self.rect.x) <= 5:
        #         tmp = 1
        #         if player.rect.x - self.rect.x < 0:
        #             tmp = -1
        #         self.rect.x += tmp
        #         #pygame.display.flip()
        #         # time.sleep(0.03)
        #         #pygame.time.wait(30)
        #     elif abs(player.rect.y - self.rect.y) <= 5:
        #         tmp = 1
        #         if player.rect.y - self.rect.y < 0:
        #             tmp = -1
        #         self.rect.y += tmp
        #         stat(player.score)
        #         pygame.display.flip()
        #         # time.sleep(0.03)
        #         pygame.time.wait(30)
        pass


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(weapon_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = sword
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 13)

    def hit_check(self):
        if pygame.sprite.spritecollideany(self, enemy_group):
            for i in range(len(enemies)):
                if pygame.sprite.collide_mask(self, enemies[i]):
                    enemies[i].taking_damage()
                    print('sdfsfsefefdsfefssfee')
                    break
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_anims['default']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 20
        )
        self.healt_init()
        self.score = 0

    def healt_init(self):
        self.current_health = 500
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 10

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
        move_speed = 2
        if key == pygame.K_a:
            if not self.checker_wall_for_left():
                for i in range(1, 5):
                    self.image = player_anims['left'][i]
                    self.rect.x -= move_speed
                    weapon.rect.x -= move_speed
                    shadow.rect.x -= move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

        elif key == pygame.K_d:
            if not self.checker_wall_for_right():
                for i in range(1, 5):
                    self.image = player_anims['right'][i]
                    self.rect.x += move_speed
                    weapon.rect.x += move_speed
                    shadow.rect.x += move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

        elif key == pygame.K_w:
            if not self.checker_wall_for_top():
                for i in range(1, 5):
                    self.image = player_anims['up'][i]
                    self.rect.y -= move_speed
                    weapon.rect.y -= move_speed
                    shadow.rect.y -= move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

        elif key == pygame.K_s:
            if not self.checker_wall_for_bottom():
                for i in range(1, 5):
                    self.image = player_anims['down'][i]
                    self.rect.y += move_speed
                    weapon.rect.y += move_speed
                    shadow.rect.y += move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

    def checker_wall_for_left(self):
        global flagD, flagU, flagL, flagR
        if pygame.sprite.spritecollideany(shadow, border_floor_left_group):
            flagL = False
            return True
        else:
            return False

    def checker_wall_for_right(self):
        global flagD, flagU, flagL, flagR
        if pygame.sprite.spritecollideany(shadow, border_floor_right_group):
            flagR = False
            return True
        else:
            return False

    def checker_wall_for_top(self):
        global flagD, flagU, flagL, flagR
        if pygame.sprite.spritecollideany(shadow, border_floor_top_group):
            flagU = False
            return True
        elif pygame.sprite.spritecollideany(shadow, door_group):
            for i in range(len(doors)):
                if pygame.sprite.collide_mask(shadow, doors[i]):
                    doors[i].open_door()
                    print('doooooooor')
        else:
            return False

    def checker_wall_for_bottom(self):
        global flagD, flagU, flagL, flagR
        if pygame.sprite.spritecollideany(shadow, border_floor_bottom_group):
            print('bottom')
            flagD = False
            return True
        elif pygame.sprite.spritecollideany(shadow, door_group):
            for i in range(len(doors)):
                if pygame.sprite.collide_mask(shadow, doors[i]):
                    doors[i].open_door()
                    print('doooooooor')
        else:
            return False

    def can_player_move2(self, key1, key2):
        move_speed = 2
        if (key1 == pygame.K_d and key2 == pygame.K_w) or (key1 == pygame.K_w and key2 == pygame.K_d):
            if not self.checker_wall_for_up_right():
                for i in range(1, 5):
                    self.image = player_anims['up_right'][i]
                    self.rect.y -= move_speed
                    self.rect.x += move_speed
                    weapon.rect.y -= move_speed
                    weapon.rect.x += move_speed
                    shadow.rect.y -= move_speed
                    shadow.rect.x += move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

        elif (key1 == pygame.K_d and key2 == pygame.K_s) or (key1 == pygame.K_s and key2 == pygame.K_d):
            if not self.checker_wall_for_right_down():
                for i in range(1, 5):
                    self.image = player_anims['right_down'][i]
                    self.rect.y += move_speed
                    self.rect.x += move_speed
                    weapon.rect.y += move_speed
                    weapon.rect.x += move_speed
                    shadow.rect.y += move_speed
                    shadow.rect.x += move_speed
                    all_sprites.draw(screen)
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

        elif (key1 == pygame.K_a and key2 == pygame.K_s) or (key1 == pygame.K_s and key2 == pygame.K_a):
            if not self.checker_wall_for_left_down():
                for i in range(1, 5):
                    self.image = player_anims['left_down'][i]
                    self.rect.y += move_speed
                    self.rect.x -= move_speed
                    weapon.rect.y += move_speed
                    weapon.rect.x -= move_speed
                    shadow.rect.y += move_speed
                    shadow.rect.x -= move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

        elif (key1 == pygame.K_a and key2 == pygame.K_w) or (key1 == pygame.K_w and key2 == pygame.K_a):
            if not self.checker_wall_for_up_left():
                for i in range(1, 5):
                    self.image = player_anims['up_left'][i]
                    self.rect.y -= move_speed
                    self.rect.x -= move_speed
                    weapon.rect.y -= move_speed
                    weapon.rect.x -= move_speed
                    shadow.rect.y -= move_speed
                    shadow.rect.x -= move_speed
                    for i in [all_sprites, shadow_checker_group, weapon_group, player_group, door_group]:
                        i.draw(screen)
                        i.update()
                    stat(player.score)
                    pygame.display.flip()
                    pygame.time.wait(20)

    def checker_wall_for_up_right(self):
        global flagR, flagL, flagU, flagD
        if pygame.sprite.spritecollideany(shadow, border_floor_right_group):
            flagR = False
            return True
        elif pygame.sprite.spritecollideany(shadow, border_floor_top_group):
            flagU = False
            return True
        else:
            return False

    def checker_wall_for_right_down(self):
        global flagR, flagL, flagU, flagD
        if pygame.sprite.spritecollideany(shadow, border_floor_right_group):
            flagR = False
            return True
        elif pygame.sprite.spritecollideany(shadow, border_floor_bottom_group):
            flagD = False
            return True
        else:
            return False

    def checker_wall_for_left_down(self):
        global flagR, flagL, flagU, flagD
        if pygame.sprite.spritecollideany(shadow, border_floor_left_group):
            flagL = False
            return True
        elif pygame.sprite.spritecollideany(shadow, border_floor_bottom_group):
            flagD = False
            return True
        else:
            return False

    def checker_wall_for_up_left(self):
        global flagR, flagL, flagU, flagD
        if pygame.sprite.spritecollideany(shadow, border_floor_left_group):
            flagL = False
            return True
        elif pygame.sprite.spritecollideany(shadow, border_floor_top_group):
            flagU = False
            return True
        else:
            return False

    def stay_on_place(self):
        for i in range(1, 5):
            self.image = player_anims['stay_on_place'][i]
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)
            door_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            door_group.update()
            stat(player.score)
            pygame.display.flip()
            pygame.time.wait(70)

    def hit(self):
        if see_U:
            hit = 0

            weapon.rect.x = self.rect.x - 16
            weapon.rect.y = self.rect.y - 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x - 8
            weapon.rect.y = self.rect.y - 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 8
            weapon.rect.y = self.rect.y - 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 16
            weapon.rect.y = self.rect.y - 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.y = self.rect.y
            weapon.rect.x = self.rect.x
            if hit > 0:
                print('sdfsf1')

        elif see_R:
            hit = 0

            weapon.rect.x = self.rect.x + 10
            weapon.rect.y = self.rect.y - 16
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 10
            weapon.rect.y = self.rect.y - 8
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 10
            weapon.rect.y = self.rect.y + 8
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 10
            weapon.rect.y = self.rect.y + 16
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.y = self.rect.y
            weapon.rect.x = self.rect.x
            if hit > 0:
                print('sdfsf2')

        elif see_D:
            hit = 0

            weapon.rect.x = self.rect.x - 16
            weapon.rect.y = self.rect.y + 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x - 8
            weapon.rect.y = self.rect.y + 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 8
            weapon.rect.y = self.rect.y + 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x + 16
            weapon.rect.y = self.rect.y + 10
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.y = self.rect.y
            weapon.rect.x = self.rect.x
            if hit > 0:
                print('sdfsf3')

        elif see_L:
            hit = 0

            weapon.rect.x = self.rect.x - 10
            weapon.rect.y = self.rect.y - 16
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x - 10
            weapon.rect.y = self.rect.y - 8
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x - 10
            weapon.rect.y = self.rect.y + 8
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.x = self.rect.x - 10
            weapon.rect.y = self.rect.y + 16
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            player_group.draw(screen)

            all_sprites.update()
            weapon_group.update()
            player_group.update()
            pygame.display.flip()
            pygame.time.wait(10)
            if weapon.hit_check():
                hit += 1

            weapon.rect.y = self.rect.y
            weapon.rect.x = self.rect.x
            if hit > 0:
                print('sdfsf4')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["DDD", "",
                  "Правила игры",
                  "Нужно убить всех демонов.",
                  "С каждым убитым демоном начисляются очки."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def end_screen():
    intro_text = ["Игра Оконченна", "",
                  f"Ваш счёт: {player.score}",
                  f"Лучший счёт: {get_best_score(player.score)}"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def stat(health):
    font = pygame.font.Font(None, 25)
    text = font.render("Score:" + str(player.score), True, pygame.Color('white'))
    screen.blit(text, (630, 20))
    text = font.render("Best score:" + str(get_best_score(player.score)), True, pygame.Color('white'))
    screen.blit(text, (630, 40))


def load_and_gen_level(name):
    global level, player, level_x, level_y, weapon, shadow, size, screen,\
        running, flagL, flagR, flagU, flagD, see_L, see_U, see_D, width, height, see_R
    level = load_level(name)
    player, level_x, level_y, weapon, shadow = generate_level(level)
    size = width, height = level_x * tile_width, level_y * tile_height
    screen = pygame.display.set_mode(size)
    running = True
    flagR = flagL = flagD = flagU = False
    see_R = True
    see_L = see_U = see_D = False
    get_best_score(player.score)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Deep Dark Dungeon (DDD)')
    # generate_dungeon('map.txt', 70, 40, 110, 50, 60)
    # level = load_level('example_map2.txt')
    level_number = 1
    load_and_gen_level(f'map{level_number}.txt')
    fps = 120
    clock = pygame.time.Clock()
    start_screen()
    pygame.mixer.music.load('Assets/Sounds/music_on_the_background.mp3')
    pygame.mixer.music.play(-1)
    get_best_score(player.score)
    while running:
        if len(enemies) == defeat_enemy and level_number == 3:
            get_best_score(player.score)
            end_screen()
            running = False
        elif len(enemies) == defeat_enemy:
            level_number += 1
            load_and_gen_level(f'map{level_number}.txt')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    see_L = True
                    see_R = see_U = see_D = False
                    flagL = True
                if event.key == pygame.K_w:
                    see_U = True
                    see_R = see_L = see_D = False
                    flagU = True
                if event.key == pygame.K_s:
                    see_D = True
                    see_R = see_U = see_L = False
                    flagD = True
                if event.key == pygame.K_d:
                    see_R = True
                    see_L = see_U = see_D = False
                    flagR = True
                if event.key == pygame.K_UP:
                    player.get_health(200)
                    pygame.mixer.music.load('Assets/Sounds/Health_player.mp3')
                    pygame.mixer.music.play()
                if event.key == pygame.K_DOWN:
                    player.get_damage(200)
                    pygame.mixer.music.load('Assets/Sounds/Damage_player.mp3')
                    pygame.mixer.music.play()
                if event.key == pygame.K_SPACE:
                    player.hit()
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
        # for i in enemies:
        #     i.update()
        screen.fill((0, 0, 0))
        draw_sprites = [all_sprites, floor_group, player_group, enemy_group, chest_group, door_group,
                        wall_inner_top_right_group, wall_inner_top_left_group, wall_side_mid_left_group,
                        wall_side_mid_right_group, wall_corner_left_group, wall_corner_right_group, wall_top_left_group,
                        wall_top_right_group, wall_top_mid_group, wall_inner_top_left_out_group, wall_top_mid_in_group,
                        wall_side_front_left_group, wall_side_front_right_group, wall_side_top_left_group,
                        wall_side_top_right_group, lava_fountain_group, lava_fountain_bottom_group,
                        lava_fountain_top_group, weapon_group, wall_front_mid_group, wall_front_right_group,
                        wall_front_left_group, shadow_checker_group, border_floor_top_group, border_floor_right_group,
                        border_floor_bottom_group, border_floor_left_group]
        for i in draw_sprites:
            i.draw(screen)
        update_sprites = [all_sprites, floor_group, player_group, door_group, chest_group, enemy_group,
                          wall_inner_top_right_group, wall_inner_top_left_group, wall_side_mid_left_group,
                          wall_side_mid_right_group, wall_corner_left_group, wall_corner_right_group,
                          wall_top_left_group, wall_top_right_group, wall_top_mid_group, wall_inner_top_left_out_group,
                          wall_top_mid_in_group, wall_side_front_left_group, wall_side_front_right_group,
                          wall_side_top_left_group, wall_side_top_right_group, lava_fountain_group,
                          lava_fountain_bottom_group, lava_fountain_top_group, weapon_group, wall_front_left_group,
                          wall_front_mid_group, wall_front_right_group, shadow_checker_group, border_floor_top_group,
                          border_floor_right_group, border_floor_bottom_group, border_floor_left_group]
        for i in update_sprites:
            i.update()
        pygame.display.flip()
    pygame.quit()
