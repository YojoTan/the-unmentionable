import pygame as pg
import pygame
import random
from random import shuffle
from classes.settings import *


class Bob(pygame.sprite.Sprite):
    def __init__(self, pos, m, l1, l2, pantalla):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.co = 0
        self.dir = 6
        self.pantalla = pantalla
        self.ls_type_animation_bob = l1
        self.ls_to_animate_enemies = l2
        self.image = self.m[self.dir][self.co]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - (self.rect[2] // 2)
        self.rect.y = pos[1] - (self.rect[3] // 2)
        self.blocks = []
        self.last_sprite = 0
        self.velx = 0
        self.vely = 0
        self.cont = 120
        self.health = 10
        self.letters = 0
        self.balas_bobs_level_2 = pygame.sprite.Group()
        self.bobl2 = True
        self.take = True
        self.death = False
        self.camera = False
        self.collide = False
        self.temp_death = 100
        self.temp = 120
        self.q = {'0': 2, '1': 2, '2': 2, '3': 0}

    def update(self):
        ls_obj = pygame.sprite.spritecollide(self, self.blocks, False)
        now = pg.time.get_ticks()
        colision = None
        if self.death is False:
            for b in ls_obj:
                self.q['3'] = 1
                if self.rect.right > b.rect.left and self.dir in [6, 8, 10]:
                    if self.velx > 0:
                        self.rect.right = b.rect.left
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Derecha"
                    elif self.camera is True:
                        if self.velx == 0:
                            self.rect.right = b.rect.left - 5
                            self.q['1'] = 1
                            self.velx = 0
                            colision = "Derecha igual"
                        elif self.velx < 0:
                            self.rect.right = b.rect.left + 5
                            self.velx = 0
                            self.q['1'] = 1
                            colision = "Derecha diferente"
                        elif self.velx > 0:
                            colision = "Error"

                elif self.rect.left < b.rect.right and self.dir in [7, 9, 11]:
                    if self.velx < 0:
                        self.rect.left = b.rect.right
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Izquierda"
                    elif self.velx > 0:
                        pass
                    elif self.camera is True:
                        if self.velx == 0:
                            self.rect.left = b.rect.right + 5
                            self.velx = 0
                            self.q['1'] = 1
                            colision = "Izquierda igual"
                        elif self.velx > 0:
                            self.rect.left = b.rect.right - 5
                            self.velx = 0
                            self.q['1'] = 1
                            colision = "Izquierda diferente"
                        elif self.velx < 0:
                            colision = "Error"

                if self.rect.bottom > b.rect.top and self.dir == 2:
                    if self.vely > 0:
                        self.rect.bottom = b.rect.top
                        self.vely = 0
                        self.q['2'] = 1
                        colision = "Abajo"
                    elif self.camera is True:
                        if self.vely >= 0:
                            self.rect.bottom = b.rect.top - 5
                            self.q['2'] = 1
                            self.vely = 0
                            colision = "Abajo igual"
                        elif self.vely < 0:
                            self.rect.bottom = b.rect.top + 5
                            self.vely = 0
                            self.q['2'] = 1
                            colision = "Abajo diferente"
                        else:
                            colision = "Error"

                elif self.rect.top < b.rect.bottom and self.dir == 3:
                    if self.vely < 0:
                        self.rect.top = b.rect.bottom
                        self.vely = 0
                        self.q['2'] = 1
                        colision = "Arriba"
                    elif self.camera is True:
                        if self.vely <= 0:
                            self.rect.top = b.rect.bottom + 5
                            self.q['2'] = 1
                            self.vely = 0
                            colision = "Arriba igual"
                        elif self.vely > 0:
                            self.rect.top = b.rect.bottom - 5
                            self.vely = 0
                            self.q['2'] = 1
                            colision = "Arriba Diferente"
                        else:
                            colision = "Error"

                if colision is not None:
                    ls_obj = []

        # Activar estado de colision
        if self.q['3'] == 1:
            moneda = random.randrange(100)
            if moneda > 50:
                self.q['1'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 33:
                    shuffle(self.ls_type_animation_bob)
                    self.dir  = self.ls_type_animation_bob[0]
                    self.velx = VELX_B
                else:
                    shuffle(self.ls_type_animation_bob)
                    self.dir = self.ls_type_animation_bob[0] + 1
                    self.velx = -VELX_B
            else:
                self.q['2'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 50:
                    self.dir = 2
                    self.vely = VELY_B
                else:
                    self.dir = 3
                    self.vely = -VELY_B

            self.q['3']=0


        #Activar el estado de cambio de dirección
        if self.cont == 0:
            moneda = random.randrange(100)
            if moneda > 50:
                self.q['1'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 33:
                    shuffle(self.ls_type_animation_bob)
                    self.dir = self.ls_type_animation_bob[0]
                    self.velx = VELX_B
                    self.vely = 0
                else:
                    shuffle(self.ls_type_animation_bob)
                    self.dir  = self.ls_type_animation_bob[0] + 1
                    self.velx = -VELX_B
                    self.vely = 0
            else:
                self.q['2'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 50:
                    self.dir = 2
                    self.vely = VELY_B
                    self.velx = 0
                else:
                    self.dir = 3
                    self.vely = -VELY_B
                    self.velx = 0

            self.cont = 120

        if self.letters == 4:
            self.take = False
        #Animación de los sprites del jugador
        if self.velx != 0 or self.vely != 0 or (self.camera is True and self.death is False):
            if now - self.last_sprite > 200:
                self.last_sprite = now
                if self.dir == 2:
                    if self.co < 2:
                        self.co += 1
                    else:
                        self.co = 0
                elif self.dir == 3:
                    if self.co < 2:
                        self.co += 1
                    else:
                        self.co = 0
                else:
                    if self.co < 8:
                        self.co += 1
                    else:
                        self.co = 0
        elif self.death:
            if self.temp_death > 10:
                if now - self.last_sprite > 300:
                    self.last_sprite = now
                    if self.co < 7:
                        self.co += 1
                    else:
                        self.co = 6
            else:
                self.co = 8
                self.dir = 12

        self.cont -= 1
        if self.bobl2 is True:
            if self.temp <= 0:
                    b = Bala_bob_level_2(self.posicion(), self.ls_to_animate_enemies)
                    if self.velx > 0:
                        b.dir = 6
                        b.velx = 5
                    if self.velx < 0:
                        b.dir = 5
                        b.velx = -5
                    if self.vely > 0:
                        b.dir = 4
                        b.vely = 5
                    if self.vely < 0:
                        b.dir = 7
                        b.vely = -5

                    self.balas_bobs_level_2.add(b)
                    self.temp = random.randrange(70, 120)

            for bala in self.balas_bobs_level_2:
                ls_obj = pygame.sprite.spritecollide(bala, self.blocks, False)
                if len(ls_obj) > 0:
                    self.balas_bobs_level_2.remove(bala)

            self.balas_bobs_level_2.update()
            self.temp -= 1

        if self.death and self.temp_death > 0:
            self.temp_death -= 1
            print(self.temp_death)

        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image = self.m[self.dir][self.co]

        if not(self.death):
            pygame.draw.rect(self.pantalla, RED, (self.rect.x, self.rect.y - 10, 40, 4))
            pygame.draw.rect(self.pantalla, GREEN, (self.rect.x, self.rect.y - 10, 40 - ((40/10)*(10-self.health)), 4))

    def posicion(self):
        #Retorna posicion
        p = [self.rect.x + 10, self.rect.y]
        return p

    def sound(self, sound):
        sound.play()
        sound.set_volume(0.5)


class Bala_bob_level_2(pygame.sprite.Sprite):
    def __init__(self, pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.co = 3
        self.dir = 4
        self.image = self.m[self.dir][self.co]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.id = 0
        self.velx = 0
        self.vely = 0
        self.last_sprite = 0

    def update(self):

        now = pg.time.get_ticks()

        if self.velx != 0 or self.vely != 0:
            if now - self.last_sprite > 100:
                self.last_sprite = now
                if self.co < 5:
                    self.co += 1
                else:
                    self.co = 3

        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image = self.m[self.dir][self.co]


class Torreta(pygame.sprite.Sprite):
    def __init__(self, pos, imagen, zona):
        pygame.sprite.Sprite.__init__(self)
        self.co = 0
        self.imagen = imagen
        self.image = self.imagen[self.co]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.activated = False
        self.vely = 0
        self.velx = 0
        self.zona = zona
        self.last_sprite = 0
        self.temp = 10
        self.bullets = pygame.sprite.Group()
        self.bulletimg = None
        self.bloques = pygame.sprite.Group()
        self.dispara = False

    def update(self):
        if self.activated is True:
            now = pg.time.get_ticks()
            if self.dispara:
                if now - self.last_sprite > 50:
                    self.last_sprite = now
                    if self.co < (len(self.imagen) - 1):
                        self.co += 1
                    else:
                        self.co = 0
            else:
                self.co = 0

            if self.temp < 0:
                self.dispara = True
                direccion = random.randrange(0, 3)
                if direccion == 0: #Torre que dispara hacia abajo
                    img_bal_tor = pygame.transform.rotate(self.bulletimg, 180)
                    velx = 0
                    vely = 5
                    moneda = random.randrange(100)
                    if moneda < 50:
                        pos = self.rect.center
                    elif moneda < 75:
                        pos = self.rect.bottomright
                    else:
                        pos = self.rect.bottomleft

                if direccion == 1:#Torre que dispara hacia la derecha
                    img_bal_tor = pygame.transform.rotate(self.bulletimg, 270)
                    velx = 5
                    vely = 0
                    moneda = random.randrange(100)
                    if moneda < 50:
                        pos = self.rect.center
                    elif moneda < 75:
                        pos = self.rect.topright
                    else:
                        pos = self.rect.bottomright

                if direccion == 2:#Torre que dispara hacia arriba
                    img_bal_tor = pygame.transform.rotate(self.bulletimg, 0)
                    velx = 0
                    vely = -5
                    moneda = random.randrange(100)
                    if moneda < 50:
                        pos = self.rect.center
                    elif moneda < 75:
                        pos = self.rect.topleft
                    else:
                        pos = self.rect.topright

                if direccion == 3:#Torre que dispara hacia la izquierda
                    img_bal_tor = pygame.transform.rotate(self.bulletimg, 90)
                    velx = -5
                    vely = 0
                    moneda = random.randrange(100)
                    if moneda < 50:
                        pos = self.rect.center
                    elif moneda < 75:
                        pos = self.rect.topleft
                    else:
                        pos = self.rect.bottomleft

                c = Bala_torreta(pos, img_bal_tor, self.bloques)
                c.velx = velx
                c.vely = vely

                self.bullets.add(c)
                self.temp = random.randrange(50, 100)
            else:
                self.dispara = False

            self.bullets.update()
            for bullet in self.bullets:
                ls_col = pygame.sprite.spritecollide(bullet, self.bloques, False)
                if len(ls_col) > 0:
                    self.bullets.remove(bullet)
            self.temp -= 1
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image = self.imagen[self.co]


class Bala_torreta(pygame.sprite.Sprite):
    def __init__(self, pos, imagen, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.bloques = bloques

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely


class Mouse(pygame.sprite.Sprite):
    def __init__(self, pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.co = 9
        self.dir = 0
        self.image = self.m[self.dir][self.co]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - (self.rect[2] // 2)
        self.rect.y = pos[1] - (self.rect[3] // 2)
        self.last_sprite = 0
        self.blocks = []
        self.velx = 0
        self.vely = 0
        self.cont = 60
        self.health = 10
        self.letters = 0
        self.take = True
        self.camera = False
        self.q = {'0': 2, '1': 2, '2': 2, '3': 0}

    def update(self):
        ls_obj = pygame.sprite.spritecollide(self, self.blocks, False)
        now = pg.time.get_ticks()
        colision = None
        if self.letters == 3:
            self.take = False

        for b in ls_obj:
            self.q['3'] = 1
            if self.rect.right > b.rect.left and self.dir == 2:
                if self.velx > 0:
                    self.rect.right = b.rect.left
                    self.velx = 0
                    self.q['1'] = 1
                    colision = "Derecha"
                elif self.camera is True:
                    if self.velx == 0:
                        self.rect.right = b.rect.left - 5
                        self.q['1'] = 1
                        self.velx = 0
                        colision = "Derecha igual"
                    elif self.velx < 0:
                        self.rect.right = b.rect.left + 5
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Derecha diferente"
                    elif self.velx > 0:
                        colision = "Error"

            elif self.rect.left < b.rect.right and self.dir == 1:
                if self.velx < 0:
                    self.rect.left = b.rect.right
                    self.velx = 0
                    self.q['1'] = 1
                    colision = "Izquierda"
                elif self.velx > 0:
                    pass
                elif self.camera is True:
                    if self.velx == 0:
                        self.rect.left = b.rect.right + 5
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Izquierda igual"
                    elif self.velx > 0:
                        self.rect.left = b.rect.right - 5
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Izquierda diferente"
                    elif self.velx < 0:
                        colision = "Error"

            if self.rect.bottom > b.rect.top and self.dir == 0:
                if self.vely > 0:
                    self.rect.bottom = b.rect.top
                    self.vely = 0
                    self.q['2'] = 1
                    colision = "Abajo"
                elif self.camera is True:
                    if self.vely >= 0:
                        self.rect.bottom = b.rect.top - 5
                        self.q['2'] = 1
                        self.vely = 0
                        colision = "Abajo igual"
                    elif self.vely < 0:
                        self.rect.bottom = b.rect.top + 5
                        self.vely = 0
                        self.q['2'] = 1
                        colision = "Abajo diferente"
                    else:
                        colision = "Error"

            elif self.rect.top < b.rect.bottom and self.dir == 3:
                if self.vely < 0:
                    self.rect.top = b.rect.bottom
                    self.vely = 0
                    self.q['2'] = 1
                    colision = "Arriba"
                elif self.camera is True:
                    if self.vely <= 0:
                        self.rect.top = b.rect.bottom + 5
                        self.q['2'] = 1
                        self.vely = 0
                        colision = "Arriba igual"
                    elif self.vely > 0:
                        self.rect.top = b.rect.bottom - 5
                        self.vely = 0
                        self.q['2'] = 1
                        colision = "Arriba Diferente"
                    else:
                        colision = "Error"

            if colision is not None:
                ls_obj = []

        # Activar estado de colision
        if self.q['3'] == 1:
            moneda = random.randrange(100)
            if moneda > 50:
                self.q['1'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 33:
                    self.dir = 2
                    self.velx = VELX_R
                else:
                    self.dir = 1
                    self.velx = -VELX_R
            else:
                self.q['2'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 50:
                    self.dir = 0
                    self.vely = VELY_R
                else:
                    self.dir = 3
                    self.vely = -VELY_R

            self.q['3'] = 0

        #Activar el estado de cambio de dirección
        if self.cont == 0:
            moneda = random.randrange(100)
            if moneda > 50:
                self.q['1'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 33:
                    self.dir = 2
                    self.velx = VELX_R
                    self.vely = 0
                else:
                    self.dir = 1
                    self.velx = -VELX_R
                    self.vely = 0
            else:
                self.q['2'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 50:
                    self.dir = 0
                    self.vely = VELY_R
                    self.velx = 0
                else:
                    self.dir = 3
                    self.vely = -VELY_R
                    self.velx = 0

            self.cont = 60

        if self.velx != 0 or self.vely != 0 or self.camera is True:
            if now - self.last_sprite > 150:
                self.last_sprite = now

                if self.co < 11:
                    self.co += 1
                else:
                    self.co = 9
                    
        self.cont -= 1
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image = self.m[self.dir][self.co]

class Runner(pygame.sprite.Sprite):
    def __init__(self,pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.co = 9 
        self.dir = 0
        self.image=self.m[self.dir][self.co] 
        self.rect=self.image.get_rect()
        self.rect.x=pos[0] - (self.rect[2] // 2)
        self.rect.y=pos[1] - (self.rect[3] // 2)
        self.last_sprite = 0
        self.blocks = []
        self.velx=0
        self.vely = 0
        self.cont = 60
        self.health = 10
        self.letters = 0
        self.take = True
        self.q = {'0':2,'1':2,'2':2,'3':0}

    def update(self):
        ls_obj=pygame.sprite.spritecollide(self, self.blocks, False)
        now = pg.time.get_ticks()
        colision = None
        if self.letters == 3:
            self.take = False

        for b in ls_obj:
            self.q['3']=1
            if self.rect.right > b.rect.left and self.dir == 2:
                if self.velx > 0:
                    self.rect.right = b.rect.left
                    self.velx = 0
                    self.q['1'] = 1
                    colision = "Derecha"
                elif self.camera is True:
                    if self.velx == 0:
                        self.rect.right = b.rect.left - 5
                        self.q['1'] = 1
                        self.velx = 0
                        colision = "Derecha igual"
                    elif self.velx < 0:
                        self.rect.right = b.rect.left + 5
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Derecha diferente"
                    elif self.velx > 0:
                        colision = "Error"                    

            elif self.rect.left < b.rect.right and self.dir == 1:
                if self.velx < 0:    
                    self.rect.left = b.rect.right
                    self.velx = 0
                    self.q['1'] = 1
                    colision = "Izquierda"
                elif self.velx > 0:
                    pass
                elif self.camera is True:
                    if self.velx == 0:
                        self.rect.left = b.rect.right + 5
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Izquierda igual"
                    elif self.velx > 0:
                        self.rect.left = b.rect.right - 5
                        self.velx = 0
                        self.q['1'] = 1
                        colision = "Izquierda diferente"
                    elif self.velx < 0:
                        colision = "Error"                                    

            if self.rect.bottom > b.rect.top and self.dir == 0:
                if self.vely > 0:
                    self.rect.bottom = b.rect.top
                    self.vely = 0
                    self.q['2'] = 1
                    colision = "Abajo"
                elif self.camera is True:
                    if self.vely >= 0:
                        self.rect.bottom = b.rect.top - 5
                        self.q['2'] = 1
                        self.vely = 0
                        colision = "Abajo igual"
                    elif self.vely < 0:
                        self.rect.bottom = b.rect.top + 5
                        self.vely = 0
                        self.q['2'] = 1
                        colision = "Abajo diferente"
                    else:
                        colision = "Error"

            elif self.rect.top < b.rect.bottom and self.dir == 3:
                if self.vely < 0:
                    self.rect.top = b.rect.bottom
                    self.vely = 0
                    self.q['2'] = 1
                    colision = "Arriba"
                elif self.camera is True:
                    if self.vely <= 0:
                        self.rect.top = b.rect.bottom + 5
                        self.q['2'] = 1
                        self.vely = 0
                        colision = "Arriba igual"
                    elif self.vely > 0:
                        self.rect.top = b.rect.bottom - 5
                        self.vely = 0
                        self.q['2'] = 1
                        colision = "Arriba Diferente"
                    else:
                        colision = "Error"                          
            
            if colision is not None:
                ls_obj = []

        # Activar estado de colision
        if self.q['3'] == 1:
            moneda=random.randrange(100)
            if moneda > 50:
                self.q['1'] = 0
                moneda2 = random.randrange(100)
                if moneda2>33:
                    self.dir  = 2
                    self.velx = VELX_R
                else:
                    self.dir  = 1
                    self.velx = -VELX_R
            else:
                self.q['2']=0
                moneda2 = random.randrange(100)
                if moneda2>50:
                    self.dir  = 0
                    self.vely= VELY_R
                else:
                    self.dir  = 3
                    self.vely= -VELY_R

            self.q['3']=0

        #Activar el estado de cambio de dirección
        if self.cont == 0:
            moneda=random.randrange(100)
            if moneda > 50:
                self.q['1'] = 0
                moneda2 = random.randrange(100)
                if moneda2 > 33:
                    self.dir  = 2
                    self.velx = VELX_R
                    self.vely = 0
                else:
                    self.dir  = 1
                    self.velx = -VELX_R
                    self.vely = 0 
            else:
                self.q['2']=0
                moneda2 = random.randrange(100)
                if moneda2 > 50:
                    self.dir  = 0
                    self.vely = VELY_R
                    self.velx = 0
                else:
                    self.dir  = 3
                    self.vely = -VELY_R
                    self.velx = 0

            self.cont = 60        

        if self.velx != 0 or self.vely !=  0 or self.camera is True:
            if now - self.last_sprite > 100:
                self.last_sprite = now

                if self.co < 11:
                    self.co += 1
                else:
                    self.co = 9

        self.cont -= 1
        self.rect.x += self.velx 
        self.rect.y += self.vely
        self.image=self.m[self.dir][self.co]        
