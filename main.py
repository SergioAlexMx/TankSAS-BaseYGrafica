import glob
from itertools import cycle
from random import randint

import pygame
from pygame.constants import K_LEFT, K_RIGHT
from pygame.time import set_timer

import colors
import tanques

pygame.init()

# Window information
display_w = 1000
display_h = 700
window = pygame.display.set_mode((display_w, display_h))

# clock
window_clock = pygame.time.Clock()
font_1 = pygame.font.SysFont('gillsans', 25)


# Load sprites


class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y, board_size, images_path):
        super(MySprite, self).__init__()
        b = Board(board_size)
        self.px = x
        self.py = y
        self.x = b.hi + 10 + 100 * x
        self.y = b.vi + 10 + 100 * y
        self.images = [pygame.image.load(img) for img in glob.glob(images_path)]
        self.index = 0
        self.rect = pygame.Rect(self.x, self.y, 90, 90)
        self.update()

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1

    def handle_event(self):
        key = pygame.key.get_pressed()
        print("llega")
        if key[K_LEFT]:
            self.rect.x -= 50

        if key[K_RIGHT]:
            self.rect.x += 50

    def move(self, dir):
        if dir == "Este":
            self.rect.x += 10
            self.rect.y += 0
            # print(self.rect.x)


class Board(object):
    def __init__(self, size):
        self.size = size
        self.sb = 100 * self.size
        self.vi = 350 - (self.sb // 2)
        self.hi = 500 - (self.sb // 2)

    def draw(self):
        c_par = 0
        c_aux = 1
        hi = self.hi
        hf = 500 + (self.sb // 2)
        vi = self.vi
        vf = 350 + (self.sb // 2)

        for i in range(vi + 10, vf + 10, 100):
            pygame.draw.rect(window, colors.RED_H, (hi, i, 10, 90))
            pygame.draw.rect(window, colors.RED_H, (hf, i, 10, 90))
            for j in range(hi + 10, hf + 10, 100):
                if c_par != 0:
                    pygame.draw.rect(window, colors.GRAY_L, (j, i, 90, 90))
                    c_par = 0
                    # self.addText("gray_l", j, i)
                    if c_aux == self.size and self.size % 2 == 0:
                        c_par = 1
                        c_aux = 0
                else:
                    pygame.draw.rect(window, colors.NEGRO_T, (j, i, 90, 90))
                    c_par = 1
                    if c_aux == self.size and self.size % 2 == 0:
                        c_par = 0
                        c_aux = 0
                    # self.addText("x=" + str(j) + "y=" + str(i), j, i)
                c_aux += 1

            # Lineas horizontales
        for i in range(hi + 10, hf + 10, 100):
            pygame.draw.rect(window, colors.RED_H, (i, vi, 90, 10))
            pygame.draw.rect(window, colors.RED_H, (i, vf, 90, 10))

    def addText(self, txt, x, y):
        window.blit(font_1.render(str(txt), True, colors.NEGRO_F), (x, y))


class StatusUI(object):
    # HUD general de juego
    def __init__(self):
        self.pos_i1 = (0, 0)
        self.size_i1 = (10, 30)
        # Vida jugador 1
        self.player_1_name = "Jugador 1"
        self.player_1_life = "100%"
        # Vida jugador 2
        self.player_2_name = "Jugador 2"
        self.player_2_life = "100%"
        # Minas jugador 1
        self.minas_j1_title = "Minas Jugador 1"
        self.minas_j1_data = "---"
        # Minas jugador 2
        self.minas_j2_title = "Minas Jugador 2"
        self.minas_j2_data = "---"
        # Instrucciones por cada tanque
        self.ins_exe = "Nada en ejecución"

    def barra_vida(self, n_player):
        if n_player == 1:
            pass
        else:
            pass

    def draw(self):
        # Contenedor de vida j1
        pygame.draw.rect(window, colors.RED_L, (0, 50, 180, 100))
        self.addText(self.player_1_name, 10, 60, colors.WHITE_M)
        self.addText(self.player_1_life, 10, 100, colors.WHITE_M)
        # Contenedor de vida j2
        pygame.draw.rect(window, colors.GREEN_AQUA, (0, 160, 180, 100))
        self.addText(self.player_2_name, 10, 170, colors.WHITE_M)
        self.addText(self.player_2_life, 10, 210, colors.WHITE_M)
        # Contenedor de minas j1 -- Lado derecho de la pantalla
        pygame.draw.rect(window, colors.ORANGE_M, (830, 50, 180, 100))
        self.addText(self.minas_j1_title, 835, 60, colors.WHITE_M)
        self.addText(self.minas_j1_data, 835, 100, colors.WHITE_M)
        # Contenedor de minas j2
        pygame.draw.rect(window, colors.ORANGE_M, (830, 160, 180, 100))
        self.addText(self.minas_j2_title, 835, 170, colors.WHITE_M)
        self.addText(self.minas_j2_data, 835, 210, colors.WHITE_M)

        # Mostrador de instrucciones
        self.addText(self.ins_exe, 200, 660, colors.WHITE_M)

    def addText(self, txt, x, y, color=colors.NEGRO_F):
        window.blit(font_1.render(str(txt), True, color), (x, y))


class MainRun(object):
    def __init__(self, dw, dh, tam_tablero=4):
        self.tam_tablero = tam_tablero
        self.dw = dw
        self.dh = dh
        self.main()

    def generar_pos(self, tablero):
        f = True
        while f:
            x = randint(0, self.tam_tablero - 1)
            y = randint(0, self.tam_tablero - 1)
            if tablero[x][y] == 0:
                f = False
        return x, y

    def dibujar_tablero(self, mat):
        for c in mat:
            print(c)

    def main(self):
        # Bandera para el while casi-inf
        stopped = False
        st = StatusUI()
        # Cargamos los archivos de los tanques (2)
        tank1_file = open("data/tanque1.dat", "r")
        tank2_file = open("data/tanque2.dat", "r")
        tank1_dat = []
        tank2_dat = []
        for t1 in tank1_file.readlines():
            tank1_dat.append(t1.replace("\n", ""))

        for t2 in tank2_file.readlines():
            tank2_dat.append(t2.replace("\n", ""))

        # Imprimimos las instrucciones capturadas
        print(tank1_dat)
        print(tank2_dat)

        # Creamos el tablero grafico y el tablero logico
        board = Board(self.tam_tablero)
        numero_filas, numero_columnas = self.tam_tablero, self.tam_tablero
        tablero = [0] * numero_filas
        for i in range(numero_filas):
            tablero[i] = [0] * numero_columnas
        self.dibujar_tablero(tablero)

        # Creamos los tanques
        p1 = self.generar_pos(tablero)
        p2 = self.generar_pos(tablero)
        t1 = tanques.Tank(1, "Rojo", 10, 10, p1)
        tablero[t1.get_x()][t1.get_y()] = t1.nombre

        t2 = tanques.Tank(2, "Rojo", 10, 10, p2)
        tablero[t2.get_x()][t2.get_y()] = t2.nombre

        tank_1 = MySprite(p1[0], p1[1], self.tam_tablero, "sprites/tanque1\\*.png")
        tank_2 = MySprite(p2[0], p2[1], self.tam_tablero, "sprites/tanque2\\*.png")
        g1 = pygame.sprite.Group(tank_1)
        g2 = pygame.sprite.Group(tank_2)

        # Seteamos las instrucciones por tanque
        t1.set_ins(tank1_dat)
        t2.set_ins(tank2_dat)
        print(t1.ins)
        print(t2.ins)

        f = True
        i = 0
        lista_tanques = [t1, t2]

        pool_tanques = cycle(lista_tanques)

        # Ruleteamos la lista
        n = randint(0, 2)
        for i in range(n):
            next(pool_tanques)
        pool_t1 = cycle(t1.get_ins())
        pool_t2 = cycle(t2.get_ins())

        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
        while not stopped:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == (pygame.USEREVENT + 2):
                    nom_tanque = next(pool_tanques).nombre
                    if nom_tanque == 1:
                        print("Tanque 1: " + next(pool_t1))
                        st.ins_exe = "Tanque 1: " + next(pool_t1)
                        # time.sleep(1)
                    elif nom_tanque == 2:
                        print("Tanque 2: " + next(pool_t2))
                        st.ins_exe = "Tanque 2: " + next(pool_t1)
                        # time.sleep(1)

            window.fill(colors.BCK_COLOR)
            board.draw()
            st.draw()
            g1.draw(window)
            g2.draw(window)
            pygame.display.flip()
            pygame.display.update()
            window_clock.tick(60)


if __name__ == "__main__":
    MainRun(display_w, display_h, 6)
