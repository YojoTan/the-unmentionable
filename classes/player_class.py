import pygame
import random
from generators_class import Activador, Pasillo
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, matriz, animales, dog, huawei):
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz    #Sprites del jugador
        self.column = 0
        self.row = 1
        self.image = self.matriz[self.column][self.row]
        self.animales = animales
        self.dog = dog
        self.huawei = huawei
        self.depositSound = pygame.mixer.Sound('efectos/deposito.wav')
        self.rect = self.image.get_rect()    #Obtengo las dimensiones de la imagen
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.health = 500
        self.blocks = []
        self.laberinto = pygame.sprite.Group()
        self.mochila = 0
        self.voto_add = 0
        self.dispara = 10
        self.gato = False
        self.perro = False
        self.phone = False
        self.collide = False
        self.camera = False
        self.gatos = pygame.sprite.Group()
        self.perros = pygame.sprite.Group()
        self.phones = pygame.sprite.Group()
        self.cont_cats = 10
        self.cont_phones = 5
        self.puestos = []
        self.pos_vot = []
        self.id_voto = 1
        self.recompensa = False
        self.activador = False
        self.post = vec(self.rect.x, self.rect.y)

    def update(self):
        ls_temp = pygame.sprite.spritecollide(self, self.blocks, False)
        ls_lab = pygame.sprite.spritecollide(self, self.laberinto, False)

        ls_obj = ls_temp + ls_lab
        for block in ls_obj:
            if type(block) is Pasillo and block.collide is False:
                pass
            else:
                if self.rect.right > block.rect.left and self.row == 1:
                    self.rect.right = block.rect.left
                    self.velx = 0
                    #print("Derecha")
                elif self.rect.left < block.rect.right and self.row == 3:
                    self.rect.left = block.rect.right
                    self.velx = 0
                    if type(block) is Activador:
                        self.blocks.remove(block)
                        self.laberinto.empty()
                        self.activador = True
                elif self.rect.top < block.rect.bottom and self.row == 0:
                    self.rect.top = block.rect.bottom
                    self.vely = 0
                elif self.rect.bottom > block.rect.top and self.row == 2:
                    #print("Abajo")
                    self.rect.bottom = block.rect.top
                    self.vely = 0
                self.collide = True

        ls_puestos = pygame.sprite.spritecollide(self, self.puestos, False)

        for puesto in ls_puestos:
            if self.rect.right > puesto.rect.left and self.row == 1:
                self.rect.right = puesto.rect.left
                self.velx = 0
                self.depositar(puesto)
            elif self.rect.left < puesto.rect.right and self.row == 3:
                self.rect.left = puesto.rect.right
                self.velx = 0
                self.depositar(puesto)
            elif self.rect.top < puesto.rect.bottom and self.row == 0:
                self.rect.top = puesto.rect.bottom
                self.vely = 0
                self.depositar(puesto)
            elif self.rect.bottom > puesto.rect.top and self.row == 2:
                self.rect.bottom = puesto.rect.top
                self.vely = 0
                self.depositar(puesto)

        if len(ls_obj) == 0:
            self.collide = False

        if self.gato is True and self.cont_cats > 0:
            if len(self.gatos) < 3:
                gato = Gato(self.rect.center, self.animales, self.row)
                self.gatos.add(gato)
                self.gato = False
                self.cont_cats -= 1

        if self.perro is True:
            if len(self.perros) < 3:
                dog = Dog(self.rect.center, self.dog, self.row)
                self.perros.add(dog)
                self.perro = False

        if self.phone is True and self.cont_phones > 0:
            if len(self.phones) < 3:
                phone = Phone(self.rect.center, self.huawei, self.row)
                self.phones.add(phone)
                self.phone = False
                self.cont_phones -= 1

        self.image = self.matriz[self.column][self.row]
        if self.velx != 0 or self.vely != 0 or self.camera is True:
            if self.column < 2:
                self.column += 1
            else:
                self.column = 0

        #Colision de las municiones
        for gato in self.gatos:
            ls_obj = pygame.sprite.spritecollide(gato, self.blocks, False)
            if len(ls_obj) > 0:
                self.gatos.remove(gato)
        for perro in self.perros:
            ls_obj = pygame.sprite.spritecollide(perro, self.blocks, False)
            if len(ls_obj) > 0:
                self.perros.remove(perro)
        for phone in self.phones:
            ls_obj = pygame.sprite.spritecollide(phone, self.blocks, False)
            if len(ls_obj) > 0:
                self.phones.remove(phone)

        #Actualizar la municion
        if len(self.gatos) > 0:
            self.gatos.update()
        if len(self.perros) > 0:
            self.perros.update()
        if len(self.phones) > 0:
            self.phones.update()

        if self.dispara > 0:
            self.dispara -= 1

        if self.velx != 0:
            self.rect.x += self.velx
        elif self.vely != 0:
            self.rect.y += self.vely
        self.post = vec(self.rect.x, self.rect.y)

    def depositar(self, puesto):
        if self.mochila <= 20 and self.mochila > 0:
            self.depositSound.play()
            self.depositSound.set_volume(0.5)
            if self.mochila >= 10:
                puesto.votos += self.mochila
                self.mochila = 0
                self.recompensa = True
            else:
                puesto.votos += self.mochila
                self.mochila = 0
            self.pos_vot = puesto.posicion()
            self.id_voto = puesto.id
            #print('depositados')

    def posicion(self):
        #Retorna posicion
        p = [self.rect.x + 10, self.rect.y]
        return p

    def impact(self, sounds):
        moneda = random.randrange(0, 2)
        sounds[moneda].play()
        sounds[moneda].set_volume(0.5)


class Gato(pygame.sprite.Sprite):
    """docstring for Gato"""
    def __init__(self, pos, matriz, rowP):
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.column = 0
        self.row = 0
        self.image = self.matriz[self.row][self.column]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - (self.rect[2] // 2)
        self.rect.y = pos[1] - (self.rect[3] // 2)
        self.velx = 0
        self.vely = 0
        self.camera = False
        self.direccion(rowP)

    def update(self):
        if self.column < 2:
            self.column += 1
        else:
            self.column = 0
        self.image = self.matriz[self.row][self.column]
        self.rect.x += self.velx
        self.rect.y += self.vely

    def direccion(self, rowP):
        if rowP == 0:
            self.row = 3
            self.vely = -5
            self.velx = 0
        elif rowP == 1:
            self.row = 2
            self.velx = 5
            self.vely = 0
        elif rowP == 2:
            self.row = 0
            self.vely = 5
            self.velx = 0
        else:
            self.row = 1
            self.velx = -5
            self.vely = 0
        self.image = self.matriz[self.row][self.column]

class Dog(pygame.sprite.Sprite):

    def __init__(self, pos, matriz, rowP):
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.column = 0
        self.row = 0
        self.image = self.matriz[self.row][self.column]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - (self.rect[2] // 2)
        self.rect.y = pos[1] - (self.rect[3] // 2)
        self.velx = 0
        self.vely = 0
        self.camera = False
        self.direccion(rowP)

    def update(self):
        if self.column < 3:
            self.column += 1
        else:
            self.column = 0
        self.image = self.matriz[self.row][self.column]
        self.rect.x += self.velx
        self.rect.y += self.vely

    def direccion(self, rowP):
        if rowP == 0:
            self.row = 2
            self.vely = -5
            self.velx = 0
        elif rowP == 1:
            self.row = 1
            self.velx = 5
            self.vely = 0
        elif rowP == 2:
            self.row = 0
            self.vely = 5
            self.velx = 0
        else:
            self.row = 3
            self.velx = -5
            self.vely = 0
        self.image = self.matriz[self.row][self.column]


class Phone(pygame.sprite.Sprite):

    def __init__(self, pos, img, rowP):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - (self.rect[2] // 2)
        self.rect.y = pos[1] - (self.rect[3] // 2)
        self.velx = 0
        self.vely = 0
        self.camera = False
        self.direccion(rowP)

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

    def direccion(self, rowP):
        if rowP == 0:
            self.vely = -5
            self.velx = 0
        elif rowP == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.velx = 5
            self.vely = 0
        elif rowP == 2:
            self.image = pygame.transform.rotate(self.image, 180)
            self.vely = 5
            self.velx = 0
        else:
            self.image = pygame.transform.rotate(self.image, 270)
            self.velx = -5
            self.vely = 0
