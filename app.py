import pygame as pg
import configparser
from classes.player_class import *
from classes.obstacles_class import *
from classes.settings import *
from classes.generators_class import *
from rewards import *
from classes.boss import *
from inventario import *


def recorte(nomimagen, cansp_ancho, cansp_alto, player=False):
    imagen = pygame.image.load(nomimagen)
    info = imagen.get_rect()
    an_img = info[2]
    al_img = info[3]
    sp_an = an_img // cansp_ancho
    sp_al = al_img // cansp_alto
    listaSp = []
    for col in range(cansp_ancho):
        listaSp.append([])
        for row in range(cansp_alto):
            if player is True:
                cuadro = imagen.subsurface((col * sp_an) + 1, (row * sp_al) + 24, 30, 40)
            else:
                cuadro = imagen.subsurface(col * sp_an, row * sp_al, 32, 32)
            listaSp[col].append(cuadro)
    return listaSp


def spriteSheet(img_name, num_row, num_column):
    image = pg.image.load(img_name)
    info = image.get_rect()
    width_img = info[2]
    height_img = info[3]
    sprites_width = width_img // num_column
    sprites_height = height_img // num_row

    #print(sprites_width, sprites_height)

    sprites_list = []
    i = 0
    while i < num_row:
        ls = []
        j = 0
        while j < num_column:
            rect = pg.transform.scale(image.subsurface(j * sprites_width, i * sprites_height, sprites_width, sprites_height), (32, 32))
            ls.append(rect)
            j += 1
        sprites_list.append(ls)
        i += 1
    return sprites_list


def move_static(ob, velx, vely, movex, limite):
    if movex is True and limite is True:
        if ob.velx < 0:
            ob.rect.x += 5
        elif ob.velx > 0:
            ob.rect.x -= 5
    elif movex is False and limite is True:
        if ob.vely < 0:
            ob.rect.y += 5
        elif ob.vely > 0:
            ob.rect.y -= 5
    ob.velx = velx
    ob.vely = vely

def move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, velx=0, vely=0, movex=None, limite=None):
    #Moviemiento de los bloques
    for b in blocks:
        move_static(b, velx, vely, movex, limite)
        if type(b) is Activador:
            for lab in b.laberinto:
                move_static(lab, velx, vely, movex, limite)

    #Movimiento de los generadores de bobs
    for gen in gens_bob:
        move_static(gen, velx, vely, movex, limite)
        #Analisis de los bobs que estan muertos, ya que cuando mueren
        #pasan a ser objetos estaticos
        for bob in gen.bobs:
            if bob.death is True:
                move_static(bob, velx, vely, movex, limite)

    #Movimiento de los generadores de ratones
    for gen in generadores_ratones:
        move_static(gen, velx, vely, movex, limite)

    #Movimiento de los generadores de runners
    for gen in generadores_runners:
        move_static(gen, velx, vely, movex, limite)

    #Moviemiento de los generadores de votos
    for gen in gens_votos:
        move_static(gen, velx, vely, movex, limite)
        for voto in gen.votos:
            move_static(voto, velx, vely, movex, limite)

    #Moviemiento de las puertas
    for door in doors:
        move_static(door, velx, vely, movex, limite)

    #Moviemiento de los puestos
    for puesto in puestos:
        move_static(puesto, velx, vely, movex, limite)
        for act in puesto.activadores:
            move_static(act, velx, vely, movex, limite)

    #Movimiento de las recompensas
    for recompensa in recompensas:
        move_static(recompensa, velx, vely, movex, limite)

    #Movimiento de las imagenes del tutorial
    for tut in tutorial:
        move_static(tut, velx, vely, movex, limite)

    #Movimiento de las torretas
    for torreta in torretas:
        move_static(torreta, velx, vely, movex, limite)


def move_assets(obj, player, move, limite):
    #Cuando el moviento de la camara es a la derecha
    if player.row == 1 and player.velx == 0:
        if move is True:
            obj.camera = True
            if obj.vely != 0:
                obj.velx = -5
            elif obj.velx == -5:
                obj.velx *= 2
            elif obj.velx == 5:
                obj.velx = 0
        else:
            obj.camera = False
            if obj.vely != 0 and obj.velx == -5:
                obj.velx = 0
                obj.rect.x -= 5
            elif obj.velx < -5:
                obj.velx = -5
            elif obj.velx == 0 and obj.vely == 0:
                obj.velx = 5

            if limite is False:
                if obj.velx == -5:
                    obj.rect.x += 5
                elif obj.velx == 5:
                    obj.rect.x -= 5
            else:
                if obj.velx == -5 or obj.vely != 0:
                    obj.rect.x += 5
                elif obj.velx == 5:
                    obj.rect.x += 5
    #Cuando el movimiento de la camara es a la izquierda
    elif player.row == 3 and player.velx == 0:
        if move is True:
            obj.camera = True
            if obj.vely != 0:
                obj.velx = 5
            elif obj.velx == -5:
                obj.velx = 0
            elif obj.velx == 5:
                obj.velx *= 2
        else:
            obj.camera = False
            if obj.vely != 0 and obj.velx == 5:
                obj.velx = 0
                obj.rect.x += 5
            elif obj.velx == 0 and obj.vely == 0:
                obj.velx = -5
            elif obj.velx > 5:
                obj.velx = 5
            if limite is False:
                if obj.velx == -5:
                    obj.rect.x += 5
                elif obj.velx == 5:
                    obj.rect.x -= 5
            else:
                if obj.velx == -5:
                    obj.rect.x += 5
                elif obj.velx == 5 or obj.vely != 0:
                    obj.rect.x -= 5
    #Manejo en Y de los objetos al mover la camara
    elif player.row == 0 and player.vely == 0:
        if move is True:
            obj.camera = True
            if obj.velx != 0:
                obj.vely = 5
            elif obj.vely == -5:
                obj.vely = 0
            elif obj.vely == 5:
                obj.vely *= 2
        else:
            obj.camera = False
            if obj.velx != 0 and obj.vely == 5:
                obj.vely = 0
                obj.rect.y += 5
            elif obj.vely == 0 and obj.velx == 0:
                obj.vely = -5
            elif obj.vely > 5:
                obj.vely = 5

            if limite is False:
                if obj.vely == -5:
                    obj.rect.y += 5
                elif obj.vely == 5:
                    obj.rect.y -= 5
            else:
                if obj.vely == -5 or obj.velx != 0:
                    obj.rect.y -= 5
                elif obj.vely == 5:
                    obj.rect.y += 5

    elif player.row == 2 and player.vely == 0:
        if move is True:
            obj.camera = True
            if obj.velx != 0:
                obj.vely = -5
            elif obj.vely == -5:
                obj.vely *= 2
            elif obj.vely == 5:
                obj.vely = 0
        else:
            obj.camera = False
            if obj.velx != 0 and obj.vely == -5:
                obj.vely = 0
                obj.rect.y -= 5
            elif obj.vely < -5:
                obj.vely = -5
            elif obj.vely == 0 and obj.velx == 0:
                obj.vely = 5
            if limite is False:
                if obj.vely == -5:
                    obj.rect.y += 5
                elif obj.vely == 5:
                    obj.rect.y -= 5
            else:
                if obj.vely == -5:
                    obj.rect.y -= 5
                elif obj.vely == 5 or obj.velx != 0:
                    obj.rect.y += 5


def move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas, move=True, limite = False):
    #Bobs que se encuentran en movimiento
    for gen in gens_bob:
        for bob in gen.bobs:
            if bob.death is False:
                move_assets(bob, player, move, limite)
                if bob.bobl2 is True:
                    for bala in bob.balas_bobs_level_2:
                        move_assets(bala, player, move, limite)
    #Ratones que se encuentran en moviemiento
    for gen in generadores_ratones:
        for mouse in gen.ratones:
            move_assets(mouse, player, move, limite)
    #Runners que se encuentran en moviemiento
    for gen in generadores_runners:
        for runner in gen.runners:
            move_assets(runner, player, move, limite)
    #Gatos que se encuentran en movimiento
    for gato in player.gatos:
        move_assets(gato, player, move, limite)
    #Perros que se encuentran en movimiento
    for dog in player.perros:
        move_assets(dog, player, move, limite)

    for phone in player.phones:
        move_assets(phone, player, move, limite)

    for torreta in torretas:
        for bullet in torreta.bullets:
            move_assets(bullet, player, move, limite)


def show_reward(id_v, player):
    moneda = random.randrange(100)
    if id_v == 1:
        r = select_reward(moneda, -100, 0, player)
    if id_v == 2:
        r = select_reward(moneda, 0, -100, player)
    if id_v == 3:
        r = select_reward(moneda, 100, 0, player)
    if id_v == 0:
        r = select_reward(moneda, 0, 0, player)
    return r


def select_reward(moneda, x, y, player):
    posx = 0
    posy = 0
    if type(player) is Player:
        posx = player.pos_vot[0] + x
        posy = player.pos_vot[1] + y
    else:
        posx = player.rect.left
        posy = player.rect.top

    if moneda < 25:
        c = Modificador_vida([posx, posy])
        #print(player.pos_vot, 'a')
    elif moneda < 50:
        c = Modificador_elim_bobs([posx, posy])
        #print(player.pos_vot, 'b')
    else:
        c = Modificador_gatos([posx, posy])
        #print(player.pos_vot, 'd')
    return c


def draw_GUI(screen, img_UI, gen_bobs, votosP):
    temp = 0
    info_cartas  = str(player.mochila)
    texto_cartas = fuente.render(info_cartas, True, [44, 62, 80])

    for b in gen_bobs:
        temp += b.cant_votos
    info_bobs    = str(temp)
    texto_bobs   = fuente.render(info_bobs, True, [44, 62, 80])

    info_celul   = str(player.cont_phones)
    texto_celul  = fuente.render(info_celul, True, [44, 62, 80])
    info_cats    = str(player.cont_cats)
    texto_cats   = fuente.render(info_cats, True, [44, 62, 80])
    info_puesto = str(votosP)
    texto_votos = fuente.render(info_puesto, True, [44, 62, 80])

    pg.draw.rect(screen, [236, 240, 241], [0, 704, 1024, 0], 80)
    screen.blit(img_UI[0], (15, 667))
    screen.blit(pygame.transform.scale(img_UI[1], (318, 20)), (50, 675))
    pygame.draw.rect(screen, [46, 204, 113], (60, 680, 300 - ((300/500)*(500-player.health)), 10))

    screen.blit(texto_cartas, [400, 671])
    screen.blit(img_UI[2], (440, 671))

    screen.blit(img_UI[2], (520, 671))
    screen.blit(img_UI[6], (530, 671))
    screen.blit(texto_votos, [490, 671])

    screen.blit(texto_bobs, [600, 671])
    screen.blit(img_UI[2], (690, 671))
    screen.blit(pygame.transform.scale(img_UI[5], (42, 42)), (650, 660))

    screen.blit(texto_celul, [850, 671])
    screen.blit(img_UI[3], (885, 671))

    screen.blit(texto_cats, [930, 671])
    screen.blit(pygame.transform.scale(img_UI[4], (32, 32)), (960, 671))


def text_box(lista, width, height):
        inter = 40
        listaTemp = []
        centro = [width // 2, height // 2]
        tamLista = len(lista) // 2
        cont = (tamLista) * -1
        for txt in lista:
            tamx = txt.get_width()
            tamy = txt.get_height()
            listaTemp.append([centro[0] - tamx // 2, (centro[1] - tamy // 2) + (cont * inter)])
            cont += 1
        return listaTemp


class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()


def add_artefacto(inventario, reward):
    agregado = False
    ls_have = []
    ls_empty = []
    for casilla in inventario.artefactos:
        if len(casilla.artefacto) != 0:
            ls_have.append(casilla)
        else:
            ls_empty.append(casilla)

    for casilla in ls_have:
        arte = None
        for fact in casilla.artefacto:
            arte = fact
        if type(reward) is type(arte):
            casilla.artefacto.add(reward)
            reward.rect.x = casilla.rect.left + 10
            reward.rect.y = casilla.rect.top + 10
            agregado = True
    if agregado is False:
        for casilla in ls_empty:
            if agregado is False:
                casilla.artefacto.add(reward)
                reward.rect.x = casilla.rect.left + 10
                reward.rect.y = casilla.rect.top + 10
                agregado = True


def main_menu(screen):
    img_sam = pygame.transform.scale(pygame.image.load('imagenes/sam.png'), (300, 850))
    img_bob = pygame.transform.scale(pygame.image.load('imagenes/cartero.png'), (400, 400))
    img_log = pygame.transform.scale(pygame.image.load('imagenes/logo.png'), (700, 200))
    fuente  = pygame.font.Font(None, 42)
    run = False
    click = False
    op = 0
    color_font   = [245, 246, 250]
    color_button = [12, 36, 97]

    while not(run):
        screen.fill(WHITE)

        play_name  = 'START'
        crdt_name  = 'CREDITS'
        crdt_htpl  = 'TUTORIAL'
        crdt_stor  = 'STORY'
        play_name  = fuente.render(play_name, True, color_font)
        crdt_name  = fuente.render(crdt_name, True, color_font)
        tuto_name  = fuente.render(crdt_htpl, True, color_font)
        stor_name  = fuente.render(crdt_stor, True, color_font)

        screen.blit(img_sam, (0,0))
        screen.blit(img_bob, (700,350))
        screen.blit(img_log, (WIDHT//2 - 700//2, 20))

        button_1 = pygame.Rect((WIDHT//2) - (200//2), 300, 200, 50)
        button_2 = pygame.Rect((WIDHT//2) - (200//2), 400, 200, 50)
        button_3 = pygame.Rect((WIDHT//2) - (200//2), 500, 200, 50)
        button_4 = pygame.Rect((WIDHT//2) - (200//2), 600, 200, 50)

        pygame.draw.rect(screen, color_button, button_1)
        pygame.draw.rect(screen, color_button, button_2)
        pygame.draw.rect(screen, color_button, button_3)
        pygame.draw.rect(screen, color_button, button_4)

        screen.blit(play_name, [((WIDHT//2))-(play_name.get_width()//2), (300+((50//2))-(play_name.get_height()//2))])
        screen.blit(crdt_name, [((WIDHT//2))-(crdt_name.get_width()//2), (400+((50//2))-(crdt_name.get_height()//2))])
        screen.blit(tuto_name, [((WIDHT//2))-(tuto_name.get_width()//2), (500+((50//2))-(tuto_name.get_height()//2))])
        screen.blit(stor_name, [((WIDHT//2))-(stor_name.get_width()//2), (600+((50//2))-(stor_name.get_height()//2))])

        mx, my = pygame.mouse.get_pos()

        if button_1.collidepoint((mx, my)):
            if click:
                op = 1
                run = True
        if button_2.collidepoint((mx, my)):
            if click:
                credits_menu(screen)
        if button_3.collidepoint((mx, my)):
            if click:
                op = 3
                run = True
        if button_4.collidepoint((mx, my)):
            if click:
                show_history(screen)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()

    if run is True and op == 0:
        pygame.quit()

    return op


def credits_menu(screen):
    r = False
    fuente2 = pygame.font.Font(None, 30)
    texto1 = fuente2.render('Un juego desarrollado por: UGame.Inc Your Life Your Game', True, WHITE)
    texto2 = fuente2.render('Jhonatan Fuentes Toro', True, WHITE)
    texto3 = fuente2.render('Yercin González Rodríguez', True, WHITE)
    texto4 = fuente2.render('Música propiedad del juego: Dead Cells.', True, WHITE)
    texto5 = fuente2.render('Todos los creditos al artista: Yoann Laulan', True, WHITE)
    texto6 = fuente2.render('Libreria Pygame ¡feliz cumpleaños # 20!', True, WHITE)
    texto7 = fuente2.render('Videojuego distribuido bajo licencia MIT', True, WHITE)
    texto8 = fuente2.render('Todos los personajes son ficción y cualquier parecido con la realidad es mera coincidencia', True, WHITE)

    listatxt = [texto1, texto2, texto3, texto4, texto5, texto6, texto7, texto8]
    listaPos = text_box(listatxt, WIDHT, HEIGHT)
    while not(r):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = True

            screen.fill(BLACK)

            for cont, txt in enumerate(listatxt):
                screen.blit(txt, listaPos[cont])

        pygame.display.flip()


def show_history(screen):
    run = False
    click = False
    num_img = 0

    img_history = [ pygame.image.load('imagenes/h_1.png'),
                    pygame.image.load('imagenes/h_2.png'),
                    pygame.image.load('imagenes/h_3.png'),
                    pygame.image.load('imagenes/h_4.png'),
                    pygame.image.load('imagenes/h_5.png'),
                    pygame.image.load('imagenes/h_6.png'),
                    pygame.image.load('imagenes/h_7.png'),
                    pygame.image.load('imagenes/h_8.png'),
                    pygame.image.load('imagenes/h_9.png'),
                    pygame.image.load('imagenes/h_10.png')
                ]

    while not(run):
        screen.fill(WHITE)
        screen.blit(img_history[num_img], (0,0))

        button_1 = pygame.Rect(853, 602, 127, 68)
        mx, my = pygame.mouse.get_pos()

        if button_1.collidepoint((mx, my)):
            if click:
                if num_img < (len(img_history) - 1):
                    num_img += 1
                else:
                    run = True

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True

        pygame.display.flip()


class Info_final(pygame.sprite.Sprite):
    def __init__(self, imagenes):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.id = 0
        self.image = self.imagenes[self.id]
        self.rect = self.image.get_rect()

    def upadate(self):
        self.image = self.imagenes[self.id]


class Tutorial(pygame.sprite.Sprite):
    def __init__(self, pos, img1, img2):
        pygame.sprite.Sprite.__init__(self)
        self.img1 = img1
        self.img2 = img2
        self.image = self.img1
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.temp = 400
        self.velx = 0
        self.vely = 0

    def update(self):
        if self.temp > 0:
            self.temp -= 1
        else:
            self.temp = 400
            if self.image == self.img1:
                self.image = self.img2
            else:
                self.image = self.img1
        self.rect.x += self.velx
        self.rect.y += self.vely


class Mensajes(pygame.sprite.Sprite):
    def __init__(self, imagenes, screen):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.image = self.imagenes[0]
        self.rect = self.image.get_rect()
        #print(self.rect)
        self.fondo = pygame.Surface((WIDHT, HEIGHT))
        self.fondo.set_alpha(150)
        self.rect.x = 0
        self.sound = None
        self.rect.y = 0
        self.id = 0
        self.temp = 200
        self.activo = False
        self.txt = False
        self.screen = screen
        self.fuente = pygame.font.Font('fuentes/Saqanone.ttf', 25)
        self.listos = []

    def update(self):
        if self.id not in self.listos:
            self.sound.play()
            self.sound.set_volume(0.5)
            self.image = self.imagenes[self.id]
            #print("HElllo")
            self.rect.x = (WIDHT // 2) - (self.image.get_width() // 2)
            self.rect.y = (HEIGHT // 2) - (self.image.get_height() // 2)
            self.listos.append(self.id)
            self.activo = True

        if self.activo is True:
            self.screen.blit(self.fondo, (0, 0))
            self.screen.blit(self.image, [self.rect.x, self.rect.y])
            if self.temp > 0:
                self.temp -= 1
            else:
                self.txt = True
        else:
            self.temp = 200
            self.txt = False

        if self.txt is True:
            txt = self.fuente.render('Presiona la barra de espacio para omitir', True, WHITE)
            self.screen.blit(txt, (self.rect.center[0] - (txt.get_width() // 2), self.rect.bottom))


def activarcodigo(cheat):
    si = True
    if len(cheat) == len(CODIGO):
        for char, ch in zip(cheat, CODIGO):
            if char != ch:
                si = False
        return si
    else:
        return False


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDHT, HEIGHT])
    fps = pygame.time.Clock()
    grupos = pygame.sprite.Group()
    #------------- Lectura del archivo----------#
    archivo = configparser.ConfigParser()
    #------------ Mapa------------#
    archivo.read('mapa.map')
    op = 2
    mensajeSound = pygame.mixer.Sound('efectos/Mensaje.wav')
    show_history(screen)#mostrar la historia al abrir el juego
    while op != 1:
        op = main_menu(screen)
        fondo = None
        mapa = None
        ls_mapa = None
        mensaje = None
        actions = True
        if op == 1:
            fondo = pygame.image.load('imagenes/Mapa.png')
            mapa = archivo.get('info', 'mapa')
            ls_mapa = mapa.split('\n')
        elif op == 3:
            fondo = pygame.image.load('imagenes/Mapa_tuto.png')
            mapa = archivo.get('info', 'tuto')
            interfaz_tuto = [pygame.image.load('mensajes/Votos.png'),
                             pygame.image.load('mensajes/Completado.png'),
                             pygame.image.load('mensajes/Municiones.png'),
                             pygame.image.load('mensajes/Recompensa.png'),
                             pygame.image.load('mensajes/Restablecer.png')]
            mensaje = Mensajes(interfaz_tuto, screen)
            mensaje.sound = mensajeSound
            grupos.add(mensaje)
            ls_mapa = mapa.split('\n')
            actions = False

        if op in [1, 3]:
            info = fondo.get_rect()
            tamx = info[2]
            tamy = info[3]
            pos_f = [0, 0]
            camaraR = False
            camaraL = False
            camaraT = False
            camaraD = False
            limiteR = 550
            limiteL = 450
            limiteT = 300
            limiteD = 400
            fvelx = 0
            fvely = 0
            pos_boss = []
            press = False
            #--------------------- Codigo -----------------------------#
            degradado = pygame.Surface([WIDHT, HEIGHT])
            degradado.fill(BLACK)
            degradado.set_alpha(150)
            smsActivado = pygame.Surface([300, 25])
            smsActivado.fill(BLACK)
            smsActivado.set_alpha(100)
            fuenteSms = pygame.font.Font('fuentes/Saqanone.ttf', 20)
            txtSms = fuenteSms.render('MUltiplicador de votos activado', False, WHITE)
            tempSms = 300

            cursor1 = Cursor()

            fuente = pygame.font.Font(None, 42)
            img_final = [pygame.image.load('imagenes/h_11.png'),
                         pygame.image.load('imagenes/h_12.png')]
            img_player = recorte('imagenes/Personaje.png', 3, 4, True)
            img_generator = recorte('imagenes/generator_bob.png', 2, 3)
            img_carta = pygame.image.load('imagenes/carta.png')
            img_huawei = pygame.image.load('imagenes/huawei.png')
            ls_to_animate_enemies = spriteSheet('imagenes/animales.png', 8, 12)
            animate_dog = spriteSheet('imagenes/Dog3.png', 9, 4)
            ls_to_animate_bob = spriteSheet('imagenes/bob.png', 15, 9)
            ls_to_animate_runner = spriteSheet('imagenes/runner.png', 8, 12)
            ls_to_animate_trump_walk = spriteSheet('imagenes/trump_walk.png', 4, 10)

            ls_type_animation_bob = [6, 8, 10]
            img_UI = [pygame.image.load('imagenes/heart.png'),
                      pygame.image.load('imagenes/bar.png'),
                      img_carta,
                      img_huawei,
                      pygame.image.load('imagenes/catt.png'),
                      pygame.image.load('imagenes/b.png'),
                      pygame.image.load('imagenes/approved.png')]
            img_torreta = [pygame.image.load('imagenes/tow.png'),
                           pygame.image.load('imagenes/tow1.png'),
                           pygame.image.load('imagenes/tow2.png')]
            imgBulletTorreta = pygame.image.load('imagenes/bullet.png')
            botones_inven = [pygame.image.load('imagenes/boton_usar1.png'),
                             pygame.image.load('imagenes/button_usar2.png'),
                             pygame.image.load('imagenes/button_borrar1.png'),
                             pygame.image.load('imagenes/button_borrar2.png')]
            tuto = [pygame.image.load('imagenes/Attack.png'),
                    pygame.image.load('imagenes/Teclas.png')]
            #img_carta = pygame.transform.scale(img_carta, (20, 16))

            #Musica de fondo
            bossMusic = pygame.mixer.music.load('sounds/boss_music.wav')
            bgMusic = pygame.mixer.Sound('sounds/bg_sound1.wav')

            #Efectos de sonido
            playerImpact = [pygame.mixer.Sound('efectos/impactoSam1.wav'),
                            pygame.mixer.Sound('efectos/impactoSam2.wav'),
                            pygame.mixer.Sound('efectos/impactoSam3.wav')]
            doorSound1 = pygame.mixer.Sound('efectos/openDoor.wav')
            doorSound2 = pygame.mixer.Sound('efectos/closeDoor.wav')
            damageBobSound = pygame.mixer.Sound('efectos/damageBob.wav')
            deleteSound = pygame.mixer.Sound('efectos/delete.wav')

            #inventarioSound = pygame.mixer.Sound('efectos/Inventario.wav')
            rewardSound = pygame.mixer.Sound('efectos/reward.wav')
            usageSound = pygame.mixer.Sound('efectos/Usar.wav')
            gatoSound = pygame.mixer.Sound('efectos/gato.wav')
            dogSound = pygame.mixer.Sound('efectos/dog.wav')

            blocks = pygame.sprite.Group()
            gens_bob = pygame.sprite.Group()
            doors = pygame.sprite.Group()
            gens_votos = pygame.sprite.Group()
            players = pygame.sprite.Group()
            generadores_ratones = pygame.sprite.Group()
            generadores_runners = pygame.sprite.Group()
            puestos = pygame.sprite.Group()
            recompensas = pygame.sprite.Group()
            activadores = pygame.sprite.Group()
            laberinto = pygame.sprite.Group()
            boss = pygame.sprite.Group()
            runners = pygame.sprite.Group()
            actPasillos = pygame.sprite.Group()
            inventarios = pygame.sprite.Group()
            tutorial = pygame.sprite.Group()
            info = pygame.sprite.Group()
            torretas = pygame.sprite.Group()

            grupos.add(blocks)
            grupos.add(gens_bob)
            grupos.add(doors)
            grupos.add(gens_votos)
            grupos.add(players)
            grupos.add(generadores_ratones)
            grupos.add(generadores_runners)
            grupos.add(puestos)
            grupos.add(recompensas)
            grupos.add(activadores)
            grupos.add(laberinto)
            grupos.add(boss)
            grupos.add(runners)
            grupos.add(actPasillos)
            grupos.add(inventarios)
            grupos.add(tutorial)
            grupos.add(info)
            grupos.add(torretas)

            inventario = Inventario([200, 100], screen, botones_inven, cursor1)
            inventario.ubicar_elementos()
            inventario.damageBob = damageBobSound
            inventario.delete = deleteSound
            inventario.usage = usageSound
            inventarios.add(inventario)

            tut = Tutorial([0, 0], tuto[0], tuto[1])
            tutorial.add(tut)

            idDoor = ''    # Identificador para cada puerta
            idGen = ''    # Identificador para cada generador de bobs
            id_puestos = 1
            idZona = ''
            ls_BlocksDoor = []    # Lista temporal para los bloques de las puertas
            pasillos = pygame.sprite.Group()    #Lista temporal para los pasillos
            votosP = 0
            for row, ls in enumerate(ls_mapa):
                for col, char in enumerate(ls):
                    if char in ['1', 'X', 'M', 'K']:     # Muros dentro del mapa
                        block = Block([col * 32, row * 32])
                        idZona = char
                        blocks.add(block)
                    elif char in ['C', 'A', 'I', 'T', 'Q', 'Z']:    # Identificadores de las puertas
                        idDoor = char
                    elif char =='L' or char == 'S':     # Orientación de la puertas en el generador
                        door = Door([col * 32, row * 32], img_generator, char, idDoor)
                        block = Block([col * 32, row * 32], color=RED, id=idDoor, dir=char)
                        ls_BlocksDoor.append(block)
                        blocks.add(block)
                        doors.add(door)
                    if char in ['X', 'M', 'K']:
                        idZona = char
                    elif char == 'R':    # Ubicación de los generadores de los ratones
                        gen_rat = Generador_ratones([col * 32, row * 32], ls_to_animate_enemies, idZona)
                        generadores_ratones.add(gen_rat)
                    elif char == '!':    # Ubicación de los generadores de los runners
                        gen_run = Generador_runner([col * 32, row * 32], ls_to_animate_runner, idZona)
                        generadores_runners.add(gen_run)
                    elif char in ['E', 'U', 'G']:    # Identificadores de cada generador de bobs
                        idGen = char
                    elif char == 'B':     # Ubicación de los generadores de bobs
                        gen_bob = Generador_bobs([col * 32, row * 32], idGen, ls_type_animation_bob, ls_to_animate_bob,ls_to_animate_enemies, screen, idZona)
                        gens_bob.add(gen_bob)
                    elif char == 'F':
                        torreta = Torreta([col * 32, row * 32], img_torreta, idZona)
                        torretas.add(torreta)
                    elif char == 'V':    # Ubicación de los generadores de votos
                        gen_votos = Generador_votos([col * 32, row * 32], img_carta, idZona)
                        gens_votos.add(gen_votos)
                    elif char == 'D':
                        votacion = Puesto_votacion([col * 32, row * 32], id_puestos)
                        id_puestos += 1
                        puestos.add(votacion)
                    elif char in ["*", "/", "$", "+"]:
                        lab = Laberinto([col * 32, row * 32], img_generator, char)
                        laberinto.add(lab)
                    elif char == 'P':
                        player = Player([col * 32, row * 32], img_player, ls_to_animate_enemies, animate_dog, img_huawei)
                        players.add(player)
                    elif char == 'J':
                        pos_boss = [col * 32, row * 32]
                    elif char in ['2', '3', '4', '8']:
                        pasillo = Pasillo([col * 32, row * 32], img_generator, char)
                        pasillos.add(pasillo)
                        blocks.add(pasillo)
                    elif char in ['5', '6', '7']:
                        actPas = ActivadorPasillo([col * 32, row * 32], id=char)
                        actPasillos.add(actPas)
                    elif char == 'W':
                        activador = Activador([col * 32, row * 32], img_carta)
                        activadores.add(activador)
                        blocks.add(activador)
            for activador in activadores:
                activador.laberinto = laberinto

            for gen in gens_bob:
                for door in doors:    #Asignacion de las puertas correspondientes para cada generador de bobs
                    if door.id in gen.idsDoor:
                        gen.doors.add(door)
                for block in ls_BlocksDoor:    #Asignacion de los bloques de las puertas para cada generador de bobs
                    if block.id in gen.idsDoor:
                        gen.blocksDoor.add(block)
                gen.blocks = blocks

            for puesto in puestos:
                for gen in gens_bob:
                    if gen.zona == puesto.zona:
                        puesto.g_bobs.add(gen)
                for gen in generadores_ratones:
                    if gen.zona == puesto.zona:
                        puesto.g_ratas.add(gen)
                for gen in generadores_runners:
                    if gen.zona == puesto.zona:
                        puesto.g_runns.add(gen)
                for gen in gens_votos:
                    if gen.zona == puesto.zona:
                        puesto.g_votos.add(gen)
                for pasillo in pasillos:
                    if puesto.idsPasillos == pasillo.id:
                        puesto.puertas.add(pasillo)
                for torreta in torretas:
                    if torreta.zona == puesto.zona:
                        puesto.torretas.add(torreta)
                for acti in actPasillos:
                    if puesto.idsActi == acti.id:
                        puesto.activadores.add(acti)
            for acti in activadores:
                for pasillo in pasillos:
                    if acti.idsPasillos == pasillo.id:
                        pasillo.collide = False
                        acti.pasillos.add(pasillo)

            for gen in generadores_ratones:
                gen.blocks = blocks

            for gen in generadores_runners:
                gen.blocks = blocks

            for torreta in torretas:
                torreta.bulletimg = imgBulletTorreta
                torreta.bloques = blocks

            player.blocks = blocks
            player.laberinto = laberinto
            player.puestos = puestos

            info_f = Info_final(img_final)
            info.add(info_f)

            inventario.player = player
            inventario.gens_bob = gens_bob
            open_inventario = False

            defeated_boss = False
            game_over = False
            running   = False
            pos_boss = []
            press = False
            dibuja_trump = False
            bgMusic.play(-1)
            bgMusic.set_volume(0.30)
            cheat = []
            activatedCheat = False
            while not running and not game_over and not defeated_boss:
                screen.blit(fondo, pos_f)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = True
                        bgMusic.fadeout(5000)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        inventario.mouse_press = True
                    if event.type == pygame.KEYDOWN:
                        if actions is True:
                            if activatedCheat is False:
                                #print(cheat)
                                cheat.append(event.key)
                                if len(cheat) > len(CODIGO):
                                    char = cheat[0]
                                    cheat.remove(char)
                            if event.key == pygame.K_RIGHT and player.vely == 0:
                                player.row = 1
                                player.velx = 5
                                player.vely = 0
                            elif event.key == pygame.K_LEFT and player.vely == 0:
                                player.row = 3
                                player.velx = -5
                                player.vely = 0
                            elif event.key == pygame.K_UP and player.velx == 0:
                                player.row = 0
                                player.velx = 0
                                player.vely = -5
                            elif event.key == pygame.K_DOWN and player.velx == 0:
                                player.row = 2
                                player.velx = 0
                                player.vely = 5
                            if event.key == pygame.K_x:
                                if player.dispara == 0:
                                    if len(player.gatos) < 3 and player.cont_cats > 0:
                                        gatoSound.play()
                                        gatoSound.set_volume(0.2)
                                    player.gato = True
                                    player.dispara = 5
                                    #Activa mensaje de tutorial
                                    if op == 3:
                                        mensaje.id = 2
                            elif event.key == pygame.K_z:
                                if player.dispara == 0:
                                    if len(player.perros) < 3:
                                        dogSound.play()
                                        dogSound.set_volume(0.2)
                                    player.perro = True
                                    player.dispara = 5
                            elif event.key == pygame.K_h:
                                if player.dispara == 0:
                                    player.phone = True
                                    player.dispara = 5
                                    #Activa mensaje de tutorial
                                    if op == 3:
                                        mensaje.id = 2
                            elif event.key == pygame.K_TAB:
                                if open_inventario is False:
                                    open_inventario = True
                                else:
                                    open_inventario = False

                        if op == 3:
                            if event.key == pygame.K_SPACE and mensaje.temp == 0:
                                mensaje.activo = False
                                if mensaje.id == 1:
                                    running = True
                                if mensaje.id == 4:
                                    mensaje.id = 1
                        elif op == 1:
                            if event.key == pygame.K_SPACE:
                                if player.activador:
                                    for i in info:
                                        if i.id < (len(i.imagenes) - 1):
                                            i.id += 1
                                            i.image = i.imagenes[i.id]
                                        else:
                                            i.id = 0
                                            dibuja_trump = True

                    if event.type == pygame.KEYUP:
                        player.velx = 0
                        player.vely = 0
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, movex=True)
                        elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                            move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, movex=False)
                        move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas, False)
                        fvelx = 0
                        fvely = 0

                activatedCheat = activarcodigo(cheat)
                players.update()

                #Activa mensaje de tutorial
                if op == 3:
                    if len(mensaje.listos) == 0:
                        mensaje.id = 0

                #Activacion de las zonas
                for puesto in puestos:
                    if puesto.id == player.id_voto:
                        votosP = puesto.votos
                        if puesto.votos >= 20:
                            doorSound1.play()
                            doorSound1.set_volume(0.3)
                            if puesto.id == 3:
                                for activador in puesto.activadores:
                                    c = Modificador_vida([activador.rect.center[0] - 100, activador.rect.center[1]])
                                    c.id = 7
                                    c.temp_pan = 1000
                                    recompensas.add(c)
                            puesto.activated = False

                            player.id_voto += 1
                            puesto.paso = True
                            player.cont_cats = 10
                            player.cont_phones = 5
                        else:
                            if puesto.activated is False:
                                puesto.activated = True

                #Detecccion entre el contacto de las ratas con los votos y el jugador
                for gen in generadores_ratones:
                    for raton in gen.ratones:
                        if raton.take:
                            for gvotos in gens_votos:
                                ls_col = pygame.sprite.spritecollide(raton, gvotos.votos, True)
                                if len(ls_col) > 0:
                                    for l in ls_col:
                                        raton.letters += 1
                                        gvotos.cant_votos -= 1
                    ls_col = pygame.sprite.spritecollide(player, gen.ratones, True)
                    if len(ls_col) > 0:
                        player.impact(playerImpact)
                        player.health -= 5
                        gen.cant_mouse -= 1
                        #print(player.health)

                #Detecccion entre el contacto de los runners con los votos y el jugador
                for gen in generadores_runners:
                    for runner in gen.runners:
                        if runner.take:
                            for gvotos in gens_votos:
                                ls_col = pygame.sprite.spritecollide(runner, gvotos.votos, True)
                                if len(ls_col) > 0:
                                    for l in ls_col:
                                        runner.letters += 1
                                        gvotos.cant_votos -= 1
                                        for puesto in puestos:
                                            if puesto.id == player.id_voto:
                                                if puesto.votos > 0:
                                                    puesto.votos -= 1

                    ls_col = pygame.sprite.spritecollide(player, gen.runners, True)
                    if len(ls_col) > 0:
                        player.impact(playerImpact)
                        player.health -= 5
                        gen.cant_runners -= 1
                        #print(player.health)

                # Detección de los proyectiles de la torreta contra el jugador
                for torreta in torretas:
                    ls_col = pygame.sprite.spritecollide(player, torreta.bullets, True)
                    if len(ls_col) > 0:
                        player.impact(playerImpact)
                        player.health -= 10

                #Detecccion entre el contacto de los bobs con los votos y el jugador
                for gen in gens_bob:
                    for bob in gen.bobs:
                        if bob.take:  #Colision con los votos
                            for gvotos in gens_votos:
                                ls_col = pygame.sprite.spritecollide(bob, gvotos.votos, True)
                                if len(ls_col) > 0:
                                    for v in ls_col:
                                        bob.letters += 1
                                        gen.cant_votos += 1
                                        if bob.velx < 0:
                                            bob.velx += 1
                                        if bob.velx > 0:
                                            bob.velx -= 1
                                        if bob.vely < 0:
                                            bob.vely += 1
                                        if bob.vely > 0:
                                            bob.vely -= 1
                                        gvotos.cant_votos -= 1
                        #Colision entre las balas de bob con el jugador
                        ls_col = pygame.sprite.spritecollide(player, bob.balas_bobs_level_2, True)
                        if len(ls_col) > 0:
                            player.impact(playerImpact)
                            player.health -= 5
                            #print(player.health)

                    #Colision entre los bobs con el jugador
                    ls_col = pygame.sprite.spritecollide(player, gen.bobs, False)

                    if len(ls_col) == 0:
                        for bob in gen.bobs:
                            bob.collide = False
                    for bob in ls_col:
                        if bob.death is False:
                            if not(bob.collide):
                                player.impact(playerImpact)
                                player.health -= 20
                                bob.collide = True
                                #print(player.health)

                for gen in gens_votos:    #Detección de el contacto entre el jugador con los votos
                    if player.mochila < 20:
                        ls_obj = pygame.sprite.spritecollide(player, gen.votos, True)
                        for voto in ls_obj:
                            if activatedCheat is True:
                                player.mochila += 20
                            else:
                                player.mochila += 1
                            gen.cant_votos -= 1
                            if player.mochila > 20:
                                dif = player.mochila - 20
                                player.mochila -= dif

                            #print(player.mochila)
                #Deteccion de los gatos contra los ratones
                for gato in player.gatos:
                    for gen in generadores_ratones:
                        ls_obj = pygame.sprite.spritecollide(gato, gen.ratones, True)
                        if len(ls_obj) > 0:
                            player.gatos.remove(gato)
                            gen.cant_mouse -= 1
                        for phone in player.phones:
                            ls_col = pygame.sprite.spritecollide(phone, gen.ratones, True)
                            if len(ls_obj) > 0:
                                player.phones.remove(phone)
                    ls_col = pygame.sprite.spritecollide(gato, generadores_ratones, True)
                    if len(ls_col) > 0:
                        player.gatos.remove(gato)

                #Deteccion de los perros contra los bobs
                for dog in player.perros:
                    for gen in gens_bob:
                        ls_col = pygame.sprite.spritecollide(dog, gen.bobs, False)

                        if len(ls_col) > 0:
                            for bob in ls_col:
                                if bob.death is False:
                                    player.perros.remove(dog)
                                    if bob.health == 0:
                                        bob.death = True
                                        bob.velx = 0
                                        bob.vely = 0
                                        bob.dir = 12
                                        #print(l.temp_death, 'Eliminar')
                                    else:
                                        if not(bob.death):
                                            bob.sound(damageBobSound)
                                            bob.health -= 1
                                        if bob.velx == 0:
                                            if bob.vely > 0:
                                                bob.rect.y -= 10
                                            else:
                                                bob.rect.y += 10
                                        if bob.vely == 0:
                                            if bob.velx > 0:
                                                bob.rect.x -= 10
                                            else:
                                                bob.rect.x += 10

                #Deteccion de los perros contra los runners
                for dog in player.perros:
                    for gen in generadores_runners:
                        ls_col = pygame.sprite.spritecollide(dog, gen.runners, False)

                        if len(ls_col) > 0:
                            player.perros.remove(dog)
                            gen.cant_runners -= 1

                    ls_col = pygame.sprite.spritecollide(dog, generadores_runners, True)
                    if len(ls_col) > 0:
                        player.perros.remove(dog)

                #Deteccion de los huawei contra los bobs
                for gen in gens_bob:
                    for phone in player.phones:
                        ls_col = pygame.sprite.spritecollide(phone, gen.bobs, True)
                        if len(ls_obj) > 0:
                            player.phones.remove(phone)

                #Deteccion de los perros contra el jefe final
                for t in boss:
                    ls_col = pygame.sprite.spritecollide(t, player.perros, True)
                    if len(ls_col) > 0:
                        if t.health_1 > 0:
                            t.health_1 -= 1
                        else:
                            t.health_2 -= 1
                    ls_col = pygame.sprite.spritecollide(t, player.phones, True)
                    if len(ls_col) > 0:
                        if t.health_1 > 0:
                            t.health_1 -= 25
                        elif t.health_2 > 0:
                            t.health_2 -= 25
                    ls_col = pygame.sprite.spritecollide(t, player.gatos, True)

                    if t.health_2 <= 0:
                        defeated_boss = True

                #Deteccion de las recompensas
                ls_mod = pygame.sprite.spritecollide(player, recompensas, True)
                for t in ls_mod:
                    #Activa mensaje de tutorial
                    if op == 3:
                        mensaje.id = 3
                    add_artefacto(inventario, t)

                #Deteccion de los trumps contra el jugador
                for t in boss:
                    ls_obj = pygame.sprite.spritecollide(player, t.balas, True)
                    if len(ls_obj) > 0:
                        player.impact(playerImpact)
                        player.health -= 100
                        #print(player.health)

                #Activar la siguiente zona al completar 20 votos
                for puesto in puestos:
                    ls_col = pygame.sprite.spritecollide(player, puesto.activadores, False)
                    if len(ls_col) > 0:
                        for act in ls_col:
                            if act.collide is False:
                                doorSound2.play()
                                doorSound2.set_volume(0.3)
                                puesto.paso = False
                                if op == 3:
                                    mensaje.id = 4
                                act.collide = True
                #********************************** Manejo de la camara *******************************************#
                if pos_f[0] < WIDHT - tamx and player.collide is False:
                    fvelx = 0
                    pos_f[0] = WIDHT - tamx
                    #print(pos_f[0])
                    move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas,tutorial, torretas, movex=True, limite=True)
                    move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas, move=False, limite=True)

                if pos_f[0] == WIDHT - tamx:
                    camaraR = False
                else:
                    camaraR = True

                if player.rect.right > limiteR and camaraR is True and player.collide is False and player.activador is not None:
                    player.rect.right = limiteR
                    player.velx = 0
                    fvelx = -5

                if pos_f[0] > 0 and player.collide is False:
                    fvelx = 0
                    pos_f[0] = 0
                    #print(pos_f[1])
                    move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, movex=True, limite=True)
                    move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas, move=False, limite=True)

                if pos_f[0] == 0:
                    camaraL = False
                else:
                    camaraL = True

                if player.rect.left < limiteL and camaraL is True and player.collide is False and player.activador is not None:
                    player.rect.left = limiteL
                    player.velx = 0
                    fvelx = 5

                #Manejo vertical de la camara
                if pos_f[1] < HEIGHT - tamy and player.collide is False:
                    fvely = 0
                    pos_f[1] = HEIGHT - tamy
                    move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas,tutorial, torretas, movex=False, limite=True)
                    move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas, move=False, limite=True)

                if pos_f[1] == HEIGHT - tamy:
                    camaraD = False
                else:
                    camaraD = True

                if player.rect.bottom > limiteD and camaraD is True and player.collide is False and player.activador is not None:
                    player.rect.bottom = limiteD
                    player.vely = 0
                    fvely = -5

                if pos_f[1] > 0 and player.collide is False:
                    fvely = 0
                    pos_f[1] = 0
                    move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, movex=False, limite=True)
                    move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas, move=False, limite=True)

                if pos_f[1] == 0:
                    camaraT = False
                else:
                    camaraT = True

                if player.rect.top < limiteT and camaraT is True and player.collide is False and player.activador is not None:
                    player.rect.top = limiteT
                    player.vely = 0
                    fvely = 5
                if player.collide is True:
                    fvelx = 0
                    fvely = 0

                #Movimiento de la camara
                if fvelx != 0 or fvely != 0:
                    if fvelx == -5:
                        move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, velx=-5,)
                    elif fvelx == 5:
                        move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, velx=5,)
                    elif fvely == -5:
                        move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, vely=-5,)
                    elif fvely == 5:
                        move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas, vely=5,)
                    move_groups_assets(gens_bob, generadores_ratones, generadores_runners, player, torretas)
                    player.camera = True

                else:
                    player.camera = False
                    move_groups_static(blocks, gens_bob, generadores_ratones, generadores_runners, gens_votos, doors, puestos, recompensas, tutorial, torretas)

                #print("Posicion en x {} posicion en y {}". format(str(pos_f[0]), str(pos_f[1])))

                if fvelx != 0:
                    pos_f[0] += fvelx
                elif fvely != 0:
                    pos_f[1] += fvely

                #Actualizacion de los grupos
                for gen in gens_bob:
                    gen.bobs.update()
                    for bob in gen.bobs:
                        if bob.temp_death == 0:
                            c = show_reward(0, bob)
                            rewardSound.play()
                            rewardSound.set_volume(0.3)
                            recompensas.add(c)
                torretas.update()
                gens_bob.update()
                gens_votos.update()
                generadores_ratones.update()
                generadores_runners.update()
                blocks.update()
                puestos.update()
                recompensas.update()
                laberinto.update()
                boss.update()
                if op == 3:
                    tutorial.update()

                for puesto in puestos:
                    if puesto.paso is False:
                        puesto.puertas.draw(screen)

                #Dibujado de los grupos
                #blocks.draw(screen)
                #gens_votos.draw(screen)
                #puestos.draw(screen)
                torretas.draw(screen)
                doors.draw(screen)
                recompensas.draw(screen)
                boss.draw(screen)
                if op == 3:
                    tutorial.draw(screen)
                #gens_bob.draw(screen)
                #gens_votos.draw(screen)
                generadores_ratones.draw(screen)
                generadores_runners.draw(screen)
                player.gatos.draw(screen)
                player.perros.draw(screen)
                player.phones.draw(screen)
                #actPasillos.draw(screen)

                if player.activador is False:
                    activadores.draw(screen)
                    laberinto.draw(screen)
                elif player.activador is True:
                    bgMusic.fadeout(5000)
                    for activador in activadores:
                        for pasillo in activador.pasillos:
                            pasillo.collide = True
                    if dibuja_trump:
                        pygame.mixer.music.play()
                        pygame.mixer.music.set_volume(1)
                        activadores.empty()
                        laberinto.empty()
                        trump = Trump_final([WIDHT // 2, HEIGHT // 2], ls_to_animate_trump_walk)
                        player.cont_phones = 50
                        trump.player = player
                        trump.pantalla = screen
                        trump.blocks = blocks
                        boss.add(trump)
                        player.activador = None

                if player.activador:
                    info.draw(screen)
                #Se dibujan las balas de trum
                for t in boss:
                    t.balas.draw(screen)
                # Se generan las recompensas
                if player.recompensa:
                    c = show_reward(player.id_voto, player)
                    rewardSound.play()
                    rewardSound.set_volume(0.3)
                    player.recompensa = False
                    recompensas.add(c)
                    player.recompensa = False

                for r in recompensas:
                    if r.temp_pan == 0:
                        recompensas.remove(r)

                for gen in gens_votos:    #Dibujado de los votos en pantalla
                    gen.votos.draw(screen)
                    if gen.txt is not None:
                        screen.blit(gen.txt, [gen.rect.x, gen.rect.y])

                for gen in gens_bob:    #Dibujado de los bobs
                    gen.bobs.draw(screen)
                    for bob in gen.bobs:
                        if bob.bobl2 is True:
                            bob.balas_bobs_level_2.draw(screen)

                for gen in generadores_ratones:
                    gen.ratones.draw(screen)

                for gen in generadores_runners:
                    gen.runners.draw(screen)

                for torreta in torretas:
                    torreta.bullets.draw(screen)

                if player.activador is False or player.activador is None:
                    players.draw(screen)

                draw_GUI(screen, img_UI, gens_bob, votosP)
                if player.health <= 0:
                    game_over = True
                    pygame.mixer.music.stop()

                if open_inventario is True:
                    screen.blit(degradado, (0, 0))
                    inventarios.draw(screen)
                    inventarios.update()

                if activatedCheat is True and tempSms > 0:
                    #print("HEllo")
                    tempSms -= 1
                    screen.blit(smsActivado, (0, 0))
                    screen.blit(txtSms, (0, 0))

                if op == 3:
                    mensaje.update()
                    if mensaje.activo is True:
                        actions = False
                    else:
                        actions = True

                pygame.display.flip()
                fps.tick(30)
                cursor1.update()

            grupos.empty()

            if game_over:
                game_over = False
                fuente2 = pygame.font.Font(None, 42)
                texto = fuente2.render('¡Game over!', True, WHITE)
                tam_h = texto.get_height()
                tam_w = texto.get_width()
                bgMusic.fadeout(5000)
                while not game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_over = True
                    screen.fill(BLACK)
                    screen.blit(texto, [WIDHT // 2 - tam_w // 2, HEIGHT // 2 - tam_h // 2])
                    pygame.display.flip()

            elif defeated_boss and op == 1:
                defeated_boss = False
                fuente2 = pygame.font.Font(None, 30)
                texto1 = fuente2.render('¡Haz salvado las elecciones! pero ¿Estás seguro que hiciste lo correcto?', True, WHITE)
                texto2 = fuente2.render('¿Realmente la humanidad tiene garantizado el mejor futuro?...', True, WHITE)
                texto3 = fuente2.render('Un juego desarrollado por: UGame.Inc Your Life Your Game', True, WHITE)
                texto4 = fuente2.render('Jhonatan Fuentes Toro', True, WHITE)
                texto5 = fuente2.render('Yercin González Rodríguez', True, WHITE)
                texto6 = fuente2.render('Música propiedad del juego: Dead Cells.', True, WHITE)
                texto7 = fuente2.render('Todos los creditos al artista: Yoann Laulan', True, WHITE)
                listatxt = [texto1, texto2, texto3, texto4, texto5, texto6, texto7]
                listaPos = text_box(listatxt, WIDHT, HEIGHT)
                while not defeated_boss:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            defeated_boss = True
                    screen.fill(BLACK)

                    for cont, txt in enumerate(listatxt):
                        screen.blit(txt, listaPos[cont])

                    pygame.display.flip()

        elif op == 2:
            credits_menu(screen)
    pygame.quit()
