from player_class import *
import pygame as pg
from settings import *
import random


class Trump_final(pygame.sprite.Sprite):
    def __init__(self, pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.co = 0
        self.dir = 1
        self.image = self.m[self.dir][self.co]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] #- (self.rect[2] // 2)
        self.rect.y = pos[1] #- (self.rect[3] // 2)
        self.blocks = []
        self.last_sprite = 0
        self.velx = 0
        self.vely = 0
        self.cont = 120
        self.health_1 = 150
        self.health_2 = 300
        self.letters = 0
        self.shoot = True
        self.death = False
        self.temp = 120
        self.player = None
        self.pantalla = None
        self.runner = False
        self.crazy = False
        self.temp_per = 15
        self.balas = pg.sprite.Group()

        self.q = {'0':2,'1':2,'2':2,'3':0, '4':0}
        self.post = vec(self.rect.x, self.rect.y)

    def update(self):
        ls_obj=pygame.sprite.spritecollide(self, self.blocks, False)
        now = pg.time.get_ticks()

        for b in ls_obj:
            self.q['3']=1
            if self.rect.right > b.rect.left and self.dir == 1:
                self.rect.right = b.rect.left
                self.velx = 0
                self.q['1'] = 1

            if self.rect.left < b.rect.right and self.dir == 3:
                self.rect.left = b.rect.right
                self.velx = 0
                self.q['1'] = 1

            if self.rect.bottom > b.rect.top and self.dir == 0:
                self.rect.bottom = b.rect.top
                self.vely = 0
                self.q['2'] = 1

            if self.rect.top < b.rect.bottom and self.dir == 2:
                self.rect.top = b.rect.bottom
                self.vely = 0
                self.q['2'] = 1

        # Activar estado de colision
        if self.q['3'] == 1:
            self.new_pos()
            self.q['3'] = 0

        #Activar el estado de cambio de dirección
        if self.cont == 0:
            self.new_pos()
            self.cont = 120
        #Activar el estado de persecución
        l = self.player.post.distance_to(self.post)
        if (l < 100) and (l > 50):
            moneda = random.randrange(100)
            if moneda > 50:
                self.runner = True
                self.crazy  = False
                if self.velx < 0 and self.player.velx > 0:
                    self.velx = -6
                    self.invincible = True

                if self.velx > 0 and self.player.velx < 0:
                    self.velx = 6
                    self.invincible = True

                if self.vely > 0 and self.player.vely < 0:
                    self.vely = 6
                    self.invincible = True

                if self.vely < 0 and self.player.vely > 0:
                    self.vely = -6
                    self.invincible = True

                if self.vely > 0 and self.player.vely > 0:
                    self.vely = -6
                    self.dir  = 2
                    self.invincible = True

                if self.vely < 0 and self.player.vely < 0:
                    self.vely = 6
                    self.dir  = 0
            else:
                self.runner = False
                self.crazy  = True

        if self.runner:
            if self.temp_per == 0:
                self.new_pos()
                self.temp_per   = 15
                self.runner     = False
                self.crazy      = False

        elif self.crazy:
            if self.temp_per == 0:
                self.new_pos()
                self.temp_per   = 15
                self.runner     = False
                self.crazy      = False

        if self.letters == 4:
            self.take = False

        #Animación de los sprites del jugador
        if self.velx != 0 or self.vely != 0:
            if now - self.last_sprite > 100:
                self.last_sprite = now
                if self.co < 9:
                    self.co += 1
                else:
                    self.co = 0
        if self.shoot:
            if self.temp <= 0:
                if self.crazy:
                    a = Bala_trump_final(self.posicion(), self.m)
                    c = Bala_trump_final(self.posicion(), self.m)
                    d = Bala_trump_final(self.posicion(), self.m)
                    e = Bala_trump_final(self.posicion(), self.m)

                    a.dir = 1
                    a.velx = 8

                    c.dir = 3
                    c.velx = -8

                    d.dir = 0
                    d.vely = 8

                    e.dir = 2
                    e.vely = -8

                    self.balas.add(a)
                    self.balas.add(c)
                    self.balas.add(d)
                    self.balas.add(e)
                    self.temp = random.randrange(70, 120)

                else:
                    b = Bala_trump_final(self.posicion(), self.m)

                    if self.velx > 0:
                        b.dir = 1
                        b.velx = 8
                    if self.velx < 0:
                        b.dir = 3
                        b.velx = -8
                    if self.vely > 0:
                        b.dir = 0
                        b.vely = 8
                    if self.vely < 0:
                        b.dir = 2
                        b.vely = -8

                    self.balas.add(b)
                    self.temp = random.randrange(70, 120)
        self.balas.update()

        for bala in self.balas:
            ls_obj = pygame.sprite.spritecollide(bala, self.blocks, False)
            if len(ls_obj) > 0:
                self.balas.remove(bala)
        self.cont -= 1
        self.temp -= 1
        self.temp_per -= 1
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image = self.m[self.dir][self.co]
        self.post = vec(self.rect.x, self.rect.y)

        if self.health_1 > 0:
            pygame.draw.rect(self.pantalla, GREEN, (self.rect.x, self.rect.y - 10, 40, 4))
            pygame.draw.rect(self.pantalla, BLUE, (self.rect.x, self.rect.y - 10, 40 - ((40 / 150) * (150 - self.health_1)), 4))

        elif self.health_2 > 0:
            pygame.draw.rect(self.pantalla, RED, (self.rect.x, self.rect.y - 10, 40, 4))
            pygame.draw.rect(self.pantalla, GREEN, (self.rect.x, self.rect.y - 10, 40 - ((40 / 300) * (300 - self.health_2)), 4))


    def posicion(self):
        #Retorna posicion
        p = [self.rect.x + 10, self.rect.y]
        return p

    def new_pos(self):
        moneda=random.randrange(100)
        if moneda > 50:
            self.q['1'] = 0
            moneda2 = random.randrange(100)
            if moneda2>33:
                self.dir  = 1
                self.velx = VELX_B
                self.vely = 0
            else:
                self.dir  = 3
                self.velx = -VELX_B
                self.vely = 0
        else:
            self.q['2']=0
            moneda2 = random.randrange(100)
            if moneda2>50:
                self.dir  = 0
                self.vely = VELY_B
                self.velx = 0
            else:
                self.dir  = 2
                self.vely = -VELY_B
                self.velx = 0

class Bala_trump_final(pygame.sprite.Sprite):
    def __init__(self,pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.co = 0
        self.dir = 0
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

        if now - self.last_sprite > 100:
            self.last_sprite = now
            if self.co < 9:
                self.co += 1
            else:
                self.co = 0

        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image=self.m[self.dir][self.co]