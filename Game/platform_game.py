# Platform Game
import pygame as pg
import numpy as np
import random
import os
import time
from settings import *
from pygame.locals import *


######## Game class
# Player class
class Player(pg.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.velx = 0
        self.vely = 0
        self.sprite_sheet = SpriteSheet(DIRECCION + 'adventurer-Sheet.png')
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.hitBox = (self.rect.x, self.rect.y, WIDTH_PLAYER, HEIGHT_PLAYER)
        self.on_floor = False
        self.walking = False
        self.jumping = False
        self.first_jump = False
        self.vision = False
        self.attack = False
        self.current_sprite = 0
        self.last_sprite = 0
        self.vel0 = 10

    def load_images(self):
        self.standing_frames = [
            self.sprite_sheet.get_image(0, 0, 50, 37),
            self.sprite_sheet.get_image(50, 0, 50, 37),
            self.sprite_sheet.get_image(100, 0, 50, 37),
            self.sprite_sheet.get_image(150, 0, 50, 37)
        ]

        self.running_frames_right = [
            self.sprite_sheet.get_image(50, 37, 50, 37),
            self.sprite_sheet.get_image(150, 37, 50, 37),
            self.sprite_sheet.get_image(200, 37, 50, 37),
            self.sprite_sheet.get_image(250, 37, 50, 37),
            self.sprite_sheet.get_image(300, 37, 50, 37)]

        self.jumping_frames = [
            self.sprite_sheet.get_image(0, 74, 50, 37),
            self.sprite_sheet.get_image(50, 74, 50, 37),
            self.sprite_sheet.get_image(100, 74, 50, 37),
            self.sprite_sheet.get_image(150, 74, 50, 37)]

        self.falling_frames = [
            self.sprite_sheet.get_image(50, 111, 50, 37),
            self.sprite_sheet.get_image(100, 111, 50, 37)]

        self.attack1_frames = [
            self.sprite_sheet.get_image(0, 259, 50, 37),
            self.sprite_sheet.get_image(50, 259, 50, 37),
            self.sprite_sheet.get_image(150, 259, 50, 37),
            self.sprite_sheet.get_image(200, 259, 50, 37),
            self.sprite_sheet.get_image(250, 259, 50, 37),
            self.sprite_sheet.get_image(300, 259, 50, 37),
            self.sprite_sheet.get_image(0, 296, 50, 37),
            self.sprite_sheet.get_image(50, 296, 50, 37),
            self.sprite_sheet.get_image(150, 296, 50, 37),
            self.sprite_sheet.get_image(200, 296, 50, 37),
            self.sprite_sheet.get_image(250, 296, 50, 37),
            self.sprite_sheet.get_image(300, 296, 50, 37),
            self.sprite_sheet.get_image(0, 333, 50, 37),
            self.sprite_sheet.get_image(50, 333, 50, 37),
            self.sprite_sheet.get_image(100, 333, 50, 37)]

        self.running_frames_left = []
        for frames in self.running_frames_right:
            self.running_frames_left.append(pg.transform.flip(frames, True, False))

        self.falling_frames_left = []
        for frames in self.falling_frames:
            self.falling_frames_left.append(pg.transform.flip(frames, True, False))

        self.standing_frames_left = []
        for frames in self.standing_frames:
            self.standing_frames_left.append(pg.transform.flip(frames, True, False))

        self.attack1_frames_left = []
        for frames in self.attack1_frames:
            self.attack1_frames_left.append(pg.transform.flip(frames, True, False))

    def update(self):
        self.animate()

        if self.on_floor == False:
            self.vely += PLAYER_GRAV
        else:
            fix_pos(1)
            self.on_floor = True

        if self.velx < 0:
            self.velx += PLAYER_FRICTION

            if self.velx > 0:
                self.velx = 0

        if self.velx > 0:
            self.velx -= PLAYER_FRICTION

            if self.velx < 0:
                self.velx = 0

        # Right
        if self.velx > 0:
            if (collide(self.rect.x + self.velx + TILE_WIDTH, self.rect.y + 1) or collide(
                    self.rect.x + self.velx + TILE_WIDTH, self.rect.y + TILE_HEIGHT - 1)):
                if (self.rect.x != int(self.rect.x / 50) * 50):
                    pass  # fix_pos(4)

                self.velx = 0

        # Left
        if self.velx < 0:
            if (collide(self.rect.x + self.velx, self.rect.y + 1) or collide(self.rect.x + self.velx,
                                                                             self.rect.y + TILE_HEIGHT - 1)):
                if (self.rect.x != int(self.rect.x / 50) * 50):
                    pass  # fix_pos(3)

                self.velx = 0

        self.rect.y += self.vely
        self.rect.x += self.velx
        # self.hitBox = (self.rect.x, self.rect.y, WIDTH_PLAYER, HEIGHT_PLAYER)

        # Floor
        if self.vely >= 0:
            if collide(self.rect.x + 1, self.rect.y + TILE_HEIGHT) or collide(self.rect.x + TILE_WIDTH - 1, self.rect.y + TILE_HEIGHT):
                fix_pos(1)
                self.vely = 0
                self.on_floor = True
            else:
                self.on_floor = False

        # Ceiling
        if self.vely < 0:
            if collide(self.rect.x + 1, self.rect.y) or collide(self.rect.x + TILE_WIDTH - 1, self.rect.y):
                #fix_pos(2)
                self.vely = 0
        pg.draw.rect(screen, RED, self.hitBox, 2)

    def animate(self):
        now = pg.time.get_ticks()
        if self.velx > 0 and self.vely == 0:
            self.walking = True
            self.vision = True
        elif self.velx < 0 and self.vely == 0:
            self.walking = True
            self.vision = False
        else:
            self.walking = False

        if self.vely != 0:

            if now - self.last_sprite > 100:
                self.last_sprite = now
                self.current_sprite = ((self.current_sprite + 1) % len(self.falling_frames))

                if self.velx > 0:
                    self.vision = True
                    self.image = self.falling_frames[self.current_sprite]
                    self.image.set_colorkey(BLACK)
                elif self.velx < 0:
                    self.vision = False
                    self.image = self.falling_frames_left[self.current_sprite]
                    self.image.set_colorkey(BLACK)
                elif self.vision:
                    self.image = self.falling_frames[self.current_sprite]
                    self.image.set_colorkey(BLACK)
                else:
                    self.image = self.falling_frames_left[self.current_sprite]
                    self.image.set_colorkey(BLACK)

        if self.walking:
            if now - self.last_sprite > 80:
                self.last_sprite = now
                self.current_sprite = ((self.current_sprite + 1) % len(self.running_frames_left))

                if self.velx > 0:
                    self.image = self.running_frames_right[self.current_sprite]
                    self.image.set_colorkey(BLACK)
                else:
                    self.image = self.running_frames_left[self.current_sprite]
                    self.image.set_colorkey(BLACK)

        if not self.walking and self.on_floor:
            if now - self.last_sprite > 150:
                self.last_sprite = now
                self.current_sprite = ((self.current_sprite + 1) % len(self.standing_frames))

                if self.vision:
                    self.image = self.standing_frames[self.current_sprite]
                    self.image.set_colorkey(BLACK)
                else:
                    self.image = self.standing_frames_left[self.current_sprite]
                    self.image.set_colorkey(BLACK)

        if self.attack:
            if now - self.last_sprite > 100:
                self.last_sprite = now
                self.current_sprite = ((self.current_sprite + 1) % len(self.attack1_frames))

                if self.vision:
                    self.image = self.attack1_frames[self.current_sprite]
                    self.image.set_colorkey(BLACK)
                else:
                    self.image = self.attack1_frames_left[self.current_sprite]
                    self.image.set_colorkey(BLACK)

                # platform class


class floor(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitBox = (self.x, self.y, 50, 50)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        pg.draw.rect(screen, (255, 0, 0), self.hitBox, 2)


# SpriteSheet class
class SpriteSheet:
    def __init__(self, file_name):
        self.spriteSheet = pg.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spriteSheet, (0, 0), (x, y, width, height))

        return image


# Camera class
class Camera:
    def __init__(self, width, heigth):
        self.camera: pg.Rect(0, 0, width, heigth)
        self.width = width
        self.heigth = heigth

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.heigth - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.heigth)


# Tileset class
class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = tile_type
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = x * 50
        self.rect.y = y * 37


####### End game class

######## Game functions
# Update windows
def redraWindow():
    screen.blit(bg, bg_rect)
    camera.update(player)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    all_sprites.update()

    pg.display.flip()


def draw_map():
    y = 0

    for layer in level_1:
        x = 0
        for tile in layer:
            if tile == 0:
                pass
            if tile == 1:
                tile_list.append(Wall(x, y, tile_floor_1))
            if tile == 2:
                tile_list.append(Wall(x, y, tile_floor_2))
            if tile == 3:
                tile_list.append(Wall(x, y, tile_floor_3))
            if tile == 4:
                tile_list.append(Wall(x, y, tile_floor_4))
            if tile == 5:
                tile_list.append(Wall(x, y, tile_floor_5))
            if tile == 6:
                tile_list.append(Wall(x, y, tile_floor_6))
            if tile == 7:
                tile_list.append(Wall(x, y, tile_floor_7))
            if tile == 8:
                tile_list.append(Wall(x, y, tile_floor_8))
            if tile == 9:
                tile_list.append(Wall(x, y, tile_floor_9))
            if tile == 10:
                tile_list.append(Wall(x, y, tile_floor_10))
            if tile == 11:
                tile_list.append(Wall(x, y, tile_floor_11))
            if tile == 12:
                tile_list.append(Wall(x, y, tile_floor_12))
            if tile == 13:
                tile_list.append(Wall(x, y, tile_floor_13))
            if tile == 14:
                tile_list.append(Wall(x, y, tile_floor_14))
            if tile == 15:
                tile_list.append(Wall(x, y, tile_floor_15))
            if tile == 16:
                tile_list.append(Wall(x, y, tile_floor_16))
            if tile == 17:
                tile_list.append(Wall(x, y, tile_floor_17))
            if tile == 18:
                tile_list.append(Wall(x, y, tile_floor_18))
            if tile == 19:
                Wall(x, y, tile_floor_bush1)
            if tile == 20:
                Wall(x, y, tile_floor_bush2)
            if tile == 21:
                Wall(x, y, tile_floor_stone)
            if tile == 22:
                Wall(x, y, tile_floor_sing1)
            if tile == 23:
                Wall(x, y, tile_floor_sing2)
            x += 1
        y += 1

    print(tile_list[0])


def collide(x, y):
    hit = False
    if 1 <= level_1[int(y / TILE_HEIGHT)][int(x / TILE_WIDTH)] <= 18:
        h = pg.sprite.spritecollide(player, tile_list, False, pg.sprite.collide_mask)
        if h:
            print('hit')
            hit = True

    return hit


def fix_pos(fix_ind):
    if fix_ind == 1:
        player.rect.y = int((player.rect.y / TILE_HEIGHT)) * TILE_HEIGHT
        # print('en 1',player.rect.y,player.rect.x, player.vely)
        # time.sleep(1)

    if fix_ind == 2:
        player.rect.y = int((player.rect.y / TILE_HEIGHT) + 1) * TILE_HEIGHT

    if fix_ind == 3:
        player.rect.x = int(player.rect.x / TILE_WIDTH) * TILE_WIDTH

    if fix_ind == 4:
        player.rect.x = int((player.rect.x / TILE_WIDTH) + 1) * TILE_WIDTH


####### End game functions

####### General settings
# initialize pygame

pg.init()
pg.mixer.init()

# initialize game window and load game graphics
pg.display.set_caption(TITLE)
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
bg = pg.image.load(DIRECCION + 'bg.png').convert()
bg_rect = bg.get_rect()
tile_list = []

tile_floor_1 = pg.transform.scale(pg.image.load(DIRECCION + '1.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_2 = pg.transform.scale(pg.image.load(DIRECCION + '2.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_3 = pg.transform.scale(pg.image.load(DIRECCION + '3.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_4 = pg.transform.scale(pg.image.load(DIRECCION + '4.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_5 = pg.transform.scale(pg.image.load(DIRECCION + '5.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_6 = pg.transform.scale(pg.image.load(DIRECCION + '6.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_7 = pg.transform.scale(pg.image.load(DIRECCION + '7.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_8 = pg.transform.scale(pg.image.load(DIRECCION + '8.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_9 = pg.transform.scale(pg.image.load(DIRECCION + '9.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_10 = pg.transform.scale(pg.image.load(DIRECCION + '10.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_11 = pg.transform.scale(pg.image.load(DIRECCION + '11.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_12 = pg.transform.scale(pg.image.load(DIRECCION + '12.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_13 = pg.transform.scale(pg.image.load(DIRECCION + '13.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_14 = pg.transform.scale(pg.image.load(DIRECCION + '14.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_15 = pg.transform.scale(pg.image.load(DIRECCION + '15.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_16 = pg.transform.scale(pg.image.load(DIRECCION + '16.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_17 = pg.transform.scale(pg.image.load(DIRECCION + '17.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_18 = pg.transform.scale(pg.image.load(DIRECCION + '18.png').convert(), (TILE_WIDTH, TILE_HEIGHT))

tile_floor_bush1 = pg.transform.scale(pg.image.load(DIRECCION + 'Bush (4).png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_bush2 = pg.transform.scale(pg.image.load(DIRECCION + 'Bush (1).png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_stone = pg.transform.scale(pg.image.load(DIRECCION + 'stone.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_sing1 = pg.transform.scale(pg.image.load(DIRECCION + 'Sign_1.png').convert(), (TILE_WIDTH, TILE_HEIGHT))
tile_floor_sing2 = pg.transform.scale(pg.image.load(DIRECCION + 'Sign_2.png').convert(), (TILE_WIDTH, TILE_HEIGHT))

# initialize clock
clock = pg.time.Clock()

# Levels
level_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 15, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 22, 0, 0, 0, 0],
    [0, 21, 0, 1, 3, 0, 19, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 17, 2, 2, 2, 0, 0, 1, 2, 2, 2, 2, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 18, 5, 5, 5, 11, 17, 5, 5, 5, 5, 5, 17, 17, 17, 17]
]

# Game loop varaibles or objetcs
run = True
player = Player(120, 259, WIDTH_PLAYER, HEIGHT_PLAYER)
camera = Camera(1000, 370)
all_sprites = pg.sprite.Group()
# walls = pg.sprite.Group()
all_sprites.add(player)
draw_map()
######## End general settings

# Game loop
while run:

    player.attack = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()
            quit()

    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()

    '''if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:
            player.attack = True'''
    if mouse[0] == 1:
        player.attack = True

    if keys[pg.K_w]:
        if player.on_floor:
            player.vely -= player.vel0
            player.on_floor = False

    if keys[pg.K_a]:
        player.velx = -3

    if keys[pg.K_d]:
        player.velx = 3

    redraWindow()
    clock.tick(FPS)