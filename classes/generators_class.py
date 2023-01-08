import pygame
import random
from classes.settings import *
from classes.enemies_class import *


class Generador_bobs(pygame.sprite.Sprite):
    def __init__(self, pos, id, l1, l2, l3, pantalla, zona, dimensiones=[32, 32]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensiones)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.pantalla = pantalla
        self.doors = pygame.sprite.Group()  # Imagenes de las puertas
        self.blocksDoor = pygame.sprite.Group()  # Bloques de las puertas
        self.bobs = pygame.sprite.Group()  # Bobs del generador
        self.blocks = []  # Bloques del mapa
        self.id = id
        self.zona = zona
        self.ls_type_animation_bob = l1
        self.ls_to_animate_bob = l2
        self.ls_to_animate_enemies = l3
        self.idsDoor = self.ids()
        self.cant_bobs = 0
        self.temp_door = 100  # Temporizador para las puertas
        self.ori = None  # Orientacion de las puertas de los generadores
        self.temp = 200  # Temporizador para generar enemigos
        self.activated = False
        self.cant_votos = 0

    def ids(self):
        if self.id == 'E':
            return ['A', 'C']
        elif self.id == 'U':
            return ['T', 'I']
        elif self.id == 'G':
            return ['Q', 'Z']

    def update(self):
        # Control sobre la generación de bobs
        # print(self.temp)
        if self.activated is True:
            if self.cant_bobs < 5:
                if self.temp > 0:
                    self.temp -= 1
                elif self.temp <= 0:
                    bob = Bob(self.rect.center, self.ls_to_animate_bob,
                              self.ls_type_animation_bob, self.ls_to_animate_enemies, self.pantalla)
                    moneda = random.randrange(100)
                    if moneda < 25:
                        shuffle(self.ls_type_animation_bob)
                        bob.dir = self.ls_type_animation_bob[0]
                        bob.velx = VELX_B
                        bob.q['0'] = 1
                        bob.q['1'] = 0
                    elif moneda < 50:
                        bob.dir = 3
                        bob.vely = -VELY_B
                        bob.q['0'] = 0
                        bob.q['2'] = 0
                    elif moneda < 75:
                        shuffle(self.ls_type_animation_bob)
                        bob.dir = self.ls_type_animation_bob[0] + 1
                        bob.velx = -VELX_B
                        bob.q['0'] = 1
                        bob.q['1'] = 0
                    else:
                        bob.dir = 2
                        bob.vely = VELY_B
                        bob.q['0'] = 0
                        bob.q['2'] = 0

                    bob.blocks = self.blocks
                    self.bobs.add(bob)
                    self.temp = 200
                    self.cant_bobs += 1
            # Control de las puertas
            if self.temp_door > 0:
                self.temp_door -= 1
            else:
                if self.temp_door < -200:
                    self.temp_door = 200
                else:
                    self.temp_door -= 1
            if self.temp_door == 0:
                order = 0
                moneda = random.randrange(100)
                if moneda < 50:
                    # #print("Open izquierda")
                    self.ori = "L"
                elif moneda <= 100:
                    # #print ("Open derecha")
                    self.ori = "S"
                for door in self.doors:
                    if door.dir == self.ori:
                        order += 1
                        if order == 1:
                            door.order = order
                        else:
                            door.order = order
                        # print(door.dir)
                        door.update(True)
                order = 0
                for block in self.blocksDoor:
                    if block.dir == self.ori:
                        order += 1
                        if order == 1:
                            block.order = order
                        else:
                            block.order = order
                        block.update(True)

            elif self.temp_door == -99:
                # print("Close {}".format(self.ori))

                for door in self.doors:
                    if door.dir == self.ori:
                        door.update(True)
                # print(len(self.blocksDoor))
                for block in self.blocksDoor:
                    if block.dir == self.ori:
                        block.update(True)
            for bob in self.bobs:
                if bob.temp_death == 0:
                    # print('Eliminar')
                    self.bobs.remove(bob)
                    self.cant_bobs -= 1

        self.doors.update()
        self.rect.x += self.velx
        self.rect.y += self.vely
        # self.bobs.update()  #Actualizacion de los bobs


class Generador_ratones(pygame.sprite.Sprite):
    def __init__(self, pos, ls, zona):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imagenes/ratas_g.png')
        self.rect = self.image.get_rect()
        self.blocks = []
        self.ratones = pygame.sprite.Group()
        self.ls_to_animate_enemies = ls
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.zona = zona
        self.velx = 0
        self.vely = 0
        self.temp = 350
        self.cant_mouse = 0
        self.activated = False

    def update(self):
        if self.activated is True:
            if self.cant_mouse < 3:
                if self.temp > 0:
                    self.temp -= 1
                else:
                    mouse = Mouse(self.rect.center, self.ls_to_animate_enemies)
                    moneda = random.randrange(100)
                    self.cant_mouse += 1
                    if moneda > 50:
                        mouse.dir = 1
                        mouse.velx = -VELX_R
                    else:
                        mouse.dir = 0
                        mouse.vely = VELY_R

                    mouse.blocks = self.blocks
                    self.ratones.add(mouse)
                    self.temp = 350

        self.ratones.update()

        self.rect.x += self.velx
        self.rect.y += self.vely


class Generador_runner(pygame.sprite.Sprite):
    def __init__(self, pos, ls, zona):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imagenes/ratas_g.png')
        self.rect = self.image.get_rect()
        self.blocks = []
        self.runners = pygame.sprite.Group()
        self.ls_to_animate_runners = ls
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.zona = zona
        self.velx = 0
        self.vely = 0
        self.temp = 350
        self.cant_runners = 0
        self.activated = False

    def update(self):
        if self.activated is True:
            if self.cant_runners < 2:
                if self.temp > 0:
                    self.temp -= 1
                else:
                    runner = Runner(self.rect.center,
                                    self.ls_to_animate_runners)
                    moneda = random.randrange(100)
                    self.cant_runners += 1

                    if moneda < 25:
                        runner.dir = 2
                        runner.velx = 5
                        runner.q['0'] = 1
                        runner.q['1'] = 0
                    elif moneda < 50:
                        runner.dir = 3
                        runner.vely = -5
                        runner.q['0'] = 0
                        runner.q['2'] = 0
                    elif moneda < 75:
                        runner.dir = 1
                        runner.velx = -5
                        runner.q['0'] = 1
                        runner.q['1'] = 0
                    else:
                        runner.dir = 0
                        runner.vely = 5
                        runner.q['0'] = 0
                        runner.q['2'] = 0

                    runner.blocks = self.blocks
                    self.runners.add(runner)
                    self.temp = 350

        self.runners.update()

        self.rect.x += self.velx
        self.rect.y += self.vely


class Generador_votos(pygame.sprite.Sprite):
    def __init__(self, pos, img, zona):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([18, 18])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.votos = pygame.sprite.Group()
        self.img = img
        self.temp = random.randrange(100, 500)
        self.txt = None
        self.cant_votos = 0
        self.limite = 4
        self.zona = zona
        self.activated = False

    def update(self):
        if self.activated is True:
            if self.cant_votos < self.limite:
                if self.temp > 0:
                    self.temp -= 1
                else:
                    moneda = random.randrange(100)
                    cant = 0
                    while cant < moneda:    # Genero la cantidad de votos
                        voto = Voto(self.rect.center, self.img)
                        self.votos.add(voto)
                        cant += 25
                        self.cant_votos += 1
                    self.temp = random.randrange(400, 500)

            if len(self.votos) > 1:     # Obtengo el numero de votos
                self.txt = self.get_txt()
            else:
                self.txt = None

        self.votos.update()
        self.rect.x += self.velx
        self.rect.y += self.vely

    def get_txt(self):
        font = pygame.font.Font(None, 30)
        txt = font.render(str(len(self.votos)), 10, BLACK)
        return txt


class Voto(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely


class Puesto_votacion(pygame.sprite.Sprite):
    def __init__(self, pos, id, dimensiones=[32, 32]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensiones)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.g_bobs = pygame.sprite.Group()
        self.g_ratas = pygame.sprite.Group()
        self.g_runns = pygame.sprite.Group()
        self.g_votos = pygame.sprite.Group()
        self.puertas = pygame.sprite.Group()
        self.activadores = pygame.sprite.Group()
        self.torretas = pygame.sprite.Group()
        self.idsPasillos = 0
        self.idsActi = 0
        self.paso = False
        self.activated = False
        self.votos = 0
        self.velx = 0
        self.vely = 0
        self.zona = None
        self.id = id
        self.ubicar()

    def update(self):
        if self.activated is False:
            for gen in self.g_bobs:
                gen.activated = False
                gen.bobs.empty()
            for gen in self.g_ratas:
                gen.activated = False
                gen.ratones.empty()
            for gen in self.g_runns:
                gen.activated = False
                gen.runners.empty()
            for gen in self.g_votos:
                gen.activated = False
                gen.votos.empty()
            for torreta in self.torretas:
                torreta.activated = False
                torreta.bullets.empty()
        elif self.activated is True:
            for gen in self.g_bobs:
                gen.activated = True
            for gen in self.g_ratas:
                gen.activated = True
            for gen in self.g_runns:
                gen.activated = True
            for gen in self.g_votos:
                gen.activated = True
            for torreta in self.torretas:
                torreta.activated = True

        if self.paso is True:
            for pas in self.puertas:
                pas.collide = False
        elif self.paso is False:
            for pas in self.puertas:
                pas.collide = True

        self.activadores.update()
        self.rect.x += self.velx
        self.rect.y += self.vely

    def ubicar(self):
        if self.id == 1:
            self.zona = 'X'
            self.idsPasillos = '2'
            self.idsActi = '5'
        elif self.id == 2:
            self.zona = 'M'
            self.idsPasillos = '3'
            self.idsActi = '6'
        elif self.id == 3:
            self.idsPasillos = '4'
            self.zona = 'K'
            self.idsActi = '7'

    def posicion(self):
        # Retorna posicion
        p = [self.rect.x, self.rect.y]
        return p


class Pasillo(pygame.sprite.Sprite):

    def __init__(self, pos, matriz, id):
        # Inicializacion del contructor de sprite
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.colum = 0
        self.row = 0
        self.image = self.matriz[self.colum][self.row]
        self.block = pygame.Surface([32, 32])
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  # Defino su posicion
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.collide = True
        self.id = id
        self.ubication()

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

    def ubication(self):
        if self.id in ['2', '4', '8']:
            self.colum = 0
            self.row = 1
        elif self.id == '3':
            self.colum = 0
            self.row = 0
        self.image = self.matriz[self.colum][self.row]


class ActivadorPasillo(pygame.sprite.Sprite):
    def __init__(self, pos, dimensiones=None, color=WHITE, id=None):
        pygame.sprite.Sprite.__init__(self)
        if dimensiones is None:
            dimensiones = [100, 100]
        self.image = pygame.Surface(dimensiones)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  # Defino su posicion
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.collide = False
        self.id = id

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely


class Activador(pygame.sprite.Sprite):

    def __init__(self, pos, img, dimensiones=[32, 32]):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.idsPasillos = '8'
        self.pasillos = pygame.sprite.Group()
        self.velx = 0
        self.vely = 0
        self.laberinto = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely


class Laberinto(pygame.sprite.Sprite):

    def __init__(self, pos, matriz, id):
        # Inicializacion del contructor de sprite
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.colum = 0
        self.row = 0
        self.image = self.matriz[self.colum][self.row]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  # Defino su posicion
        self.rect.y = pos[1]
        self.id = id
        self.orientacion()
        self.velx = 0
        self.vely = 0

    def orientacion(self):
        if self.id == "*":
            self.colum = 0
            self.row = 0
        elif self.id == "/":
            self.colum = 1
            self.row = 0
        elif self.id == "+":
            self.colum = 0
            self.row = 1
        elif self.id == "$":
            self.colum = 1
            self.row = 1
        self.image = self.matriz[self.colum][self.row]

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
