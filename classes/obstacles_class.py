import pygame
from classes.settings import *


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, dimensiones=None, color=WHITE, id=None, dir=None):
        pygame.sprite.Sprite.__init__(self)  # Inicializacion del contructor de sprite
        if dimensiones is None:
            dimensiones = [18, 18]
        self.image = pygame.Surface(dimensiones)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.prop = [abs(32 - dimensiones[0]) // 2, abs(32 - dimensiones[1]) // 2]
        self.rect.x = pos[0] + self.prop[0]  # Defino su posicion
        self.rect.y = pos[1] + self.prop[1]
        self.velx = 0
        self.vely = 0
        self.id = id
        self.dir = dir
        self.open = False
        self.order = 0

    def update(self, door=None):
        if self.id is not None and door is not None:
            if self.open is False:
                if self.dir == 'L':
                    if self.order == 2:
                        self.rect.x -= 32
                        self.rect.y -= 32
                elif self.dir == 'S':
                    if self.order == 1:
                        self.rect.x += 32
                        self.rect.y += 32
                self.open = True
            else:
                if self.dir == 'L':
                    if self.order == 2:
                        self.rect.x += 32
                        self.rect.y += 32
                elif self.dir == 'S':
                    if self.order == 1:
                        self.rect.x -= 32
                        self.rect.y -= 32
                self.open = False
        if door is None:
            self.rect.x += self.velx
            self.rect.y += self.vely


class Door(pygame.sprite.Sprite):
    def __init__(self, pos, matriz, dir, id):
        pygame.sprite.Sprite.__init__(self)  # Inicializacion del contructor de sprite
        self.matriz = matriz
        self.colum = 0
        self.row = 0
        self.dir = dir
        self.ubication()
        self.image = self.matriz[self.colum][self.row]
        self.block = pygame.Surface([32, 32])
        self.block.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  # Defino su posicion
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.open = False
        self.id = id
        self.order = 0

    def ubication(self):
        if self.dir == 'L' or self.dir == 'S':
            self.colum = 0
            self.row = 1

    def update(self, update=False):
        if update:
            if self.open is False:    #Evaluo si la puerta esta abierta
                if self.dir == 'L':
                    if self.order == 1:
                        self.colum = 1
                        self.row = 2
                    else:
                        self.colum = 0
                        self.row = 2
                        self.rect.x -= 32
                        self.rect.y -= 32
                elif self.dir == 'S':
                    if self.order == 2:
                        self.colum = 0
                        self.row = 2
                    else:
                        self.colum = 1
                        self.row = 2
                        self.rect.x += 32
                        self.rect.y += 32
                self.open = True
            else:
                self.colum = 0
                self.row = 1
                if self.dir == 'L':
                    if self.order == 2:
                        self.rect.x += 32
                        self.rect.y += 32
                elif self.dir == 'S':
                    if self.order == 1:
                        self.rect.x -= 32
                        self.rect.y -= 32
                self.open = False
            self.image = self.matriz[self.colum][self.row]

        if update is False:
            self.rect.x += self.velx
            self.rect.y += self.vely
