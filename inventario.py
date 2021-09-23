import pygame
from classes.settings import *
import random


class Casilla(pygame.sprite.Sprite):
    def __init__(self, pos, screen, cursor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imagenes/Casilla.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.artefacto = pygame.sprite.Group()
        self.cantidad = 0
        self.screen = screen
        self.cursor = cursor
        self.fondo = pygame.Surface((self.rect[1], self.rect[2]))
        self.fondo.set_alpha(150)
        self.botones = pygame.sprite.Group()
        self.fuente = pygame.font.Font('Fuentes/Saqanone.ttf', 15)
        self.texto_vacio = self.fuente.render('Vacio', False, WHITE)
        self.marco = pygame.image.load('imagenes/Marco.png')
        self.mouse_press = False

    def update(self):
        if self.cantidad != 0:
            info_canti = str(self.cantidad)
            texto_canti = self.fuente.render(info_canti, False, WHITE)
            arte = None
            for art in self.artefacto:
                arte = art
            if len(self.artefacto) > 0:
                self.screen.blit(self.marco, [arte.rect.left - 4, arte.rect.top - 4])
                self.screen.blit(texto_canti, [arte.rect.right + 75, arte.rect.bottom])
                self.screen.blit(arte.description, [arte.rect.right, arte.rect.bottom])
            for boton in self.botones:
                boton.update(self.cursor)
                boton.mouse_press = self.mouse_press
            self.artefacto.draw(self.screen)
        else:
            for boton in self.botones:
                boton.image = boton.img_normal
            self.screen.blit(self.fondo, (self.rect.x, self.rect.y))
            pos_txtx = self.rect.center[0] - self.texto_vacio.get_width() // 2
            pos_txty = self.rect.center[1] - self.texto_vacio.get_height() // 2
            self.screen.blit(self.texto_vacio, (pos_txtx, pos_txty))

        self.cantidad = len(self.artefacto)
        self.botones.draw(self.screen)


class Boton(pygame.sprite.Sprite):
    def __init__(self, pos, img1, img2):
        pygame.sprite.Sprite.__init__(self)
        self.img_normal = img1
        self.img_select = img2
        self.id = 0
        self.image = self.img_normal
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mouse_press = False
        self.action = False

    def update(self, cursor):
        if cursor.colliderect(self.rect):
            self.image = self.img_select
            if self.mouse_press is True:
                self.action = True
                self.image = self.img_normal
        else:
            self.image = self.img_normal


class Inventario(pygame.sprite.Sprite):
    def __init__(self, pos, screen, botones, cursor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imagenes/Inventario.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.screen = screen
        self.damageBob = None
        self.delete = None
        self.usage = None
        self.cursor = cursor
        self.cant_elem = 6
        self.botones = botones
        self.artefactos = pygame.sprite.Group()
        self.crear_casillas()
        self.mouse_press = False
        self.player = None
        self.gens_bobs = None

    def update(self):
        self.artefactos.draw(self.screen)
        for casilla in self.artefactos:
            casilla.update()
            casilla.mouse_press = self.mouse_press
            if len(casilla.artefacto) != 0:
                for boton in casilla.botones:
                    if boton.action is True:
                        self.execute_reward(casilla, boton.id)
                        boton.action = False
        self.mouse_press = False

    def crear_casillas(self):
        for num in range(0, self.cant_elem):
            casilla = Casilla([0, 0], self.screen, self.cursor)
            self.artefactos.add(casilla)

    def ubicar_elementos(self):
        posy = self.image.get_height() // 4
        posx = self.image.get_width() // 3
        tempx = posx + 15
        tempy = posy + 25
        x = tempx
        for num, elemn in enumerate(self.artefactos):
            elemn.rect.x = tempx
            elemn.rect.y = tempy
            tempx += posx
            if num == 2:
                tempx = x
                tempy += posy + 100
            boton1 = Boton([elemn.rect.left, elemn.rect.bottom], self.botones[0], self.botones[1])
            boton2 = Boton([elemn.rect.left + 90, elemn.rect.bottom], self.botones[2], self.botones[3])
            boton1.id = 0
            boton2.id = 1
            elemn.botones.add(boton1)
            elemn.botones.add(boton2)

    def execute_reward(self, casilla, boton):
        reward = None
        for artefacto in casilla.artefacto:
            reward = artefacto
        if boton == 0:
            self.usage.play()
            self.usage.set_volume(0.5)
            #Deteccion de las recompensas para añadirla al inventario
            if reward.id == 0:
                if self.player.health < 500 and self.player.health > 0:
                    if self.player.health == 495:
                        self.player.health += 5
                    else:
                        self.player.health += 10
            elif reward.id == 1:
                for gen in self.gens_bob:
                    for bob in gen.bobs:
                        moneda = random.randrange(100)
                        if moneda > 50:
                            bob.sound(self.damageBob)
                            bob.health -= 3
                            #print('reduce vida Bob')
            elif reward.id == 3:
                self.player.cont_cats += 2

            elif reward.id == 7:
                self.player.health = 500

            casilla.artefacto.remove(reward)
        elif boton == 1:
            self.delete.play()
            self.delete.set_volume(0.5)
            casilla.artefacto.remove(reward)
