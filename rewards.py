import pygame as pg


class Modificador_vida(pg.sprite.Sprite):
    def __init__(self, pos, dimensiones=[20, 20]):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('imagenes/heart.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.description = pg.image.load('mensajes/SaludDesc.png')
        self.id = 0
        self.velx = 0
        self.vely = 0
        self.temp_pan = 60

    def update(self):
        self.temp_pan -= 1
        self.rect.x += self.velx
        self.rect.y += self.vely


class Modificador_elim_bobs(pg.sprite.Sprite):
    def __init__(self, pos, dimensiones=[20, 20]):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('imagenes/lightning.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.id = 1
        self.description = pg.image.load('mensajes/BobsDesc.png')
        self.velx = 0
        self.vely = 0
        self.temp_pan = 60

    def update(self):
        self.temp_pan -= 1
        self.rect.x += self.velx
        self.rect.y += self.vely


class Modificador_gatos(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load('imagenes/catt.png'), (32 , 32))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 5
        self.id = 3
        self.description = pg.image.load('mensajes/GatosDesc.png')
        self.velx = 0
        self.vely = 0
        self.temp_pan = 60

    def update(self):
        self.temp_pan -= 1
        self.rect.x += self.velx
        self.rect.y += self.vely
