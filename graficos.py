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

# Constantes de vida
MINA_EXPLOTADO = 30
# clock
window_clock = pygame.time.Clock()
font_1 = pygame.font.SysFont('gillsans', 25)


# Load sprites

class Mina(object):
    def __init__(self, id, x, y, board_size):
        b = Board(board_size)
        self.id = id
        self.x = b.hi + 10 + 100 * (x)
        self.y = b.vi + 10 + 100 * (y)
        self.index = 0
        self.image = pygame.image.load("sprites/mina/mina90.png").convert_alpha()
        self.blanca = pygame.image.load("sprites/mina/image_blanca.png").convert_alpha()
        self.flag = False

    def draw(self):
        if self.flag:
            window.blit(self.image, (self.x, self.y))
        else:
            window.blit(self.blanca, (self.x, self.y))

    def set_visible(self, flag):
        self.flag = flag


class TankPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, board_size, images_path):
        super(TankPlayer, self).__init__()
        b = Board(board_size)
        self.px = x
        self.py = y
        self.x = b.hi + 10 + 100 * x
        self.y = b.vi + 10 + 100 * y
        self.images = [pygame.image.load(img) for img in glob.glob(images_path)]
        self.index = 0
        self.rect = pygame.Rect(self.x, self.y, 90, 90)
        self.update(0)

    def update(self, grad):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.image, grad)
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
            self.rect.x += 5
            self.rect.y += 0
        elif dir == "Norte":
            self.rect.x += 0
            self.rect.y += -5
        elif dir == "Sur":
            self.rect.x += 0
            self.rect.y += 5
        elif dir == "Oeste":
            self.rect.x += -5
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
                if c_par is not 0:
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
        # px
        self.px1_title = "Tanque 1 PX"
        self.px2_title = "Tanque 2 PX"
        self.px1_data = "--"
        self.px2_data = "--"

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

        # Contenedor de px 1
        pygame.draw.rect(window, colors.NEGRO_T, (830, 270, 180, 100))
        self.addText(self.px1_title, 835, 280, colors.WHITE_M)
        self.addText(self.px1_data, 835, 320, colors.WHITE_M)

        pygame.draw.rect(window, colors.NEGRO_T, (830, 380, 180, 100))
        self.addText(self.px2_title, 835, 390, colors.WHITE_M)
        self.addText(self.px2_data, 835, 430, colors.WHITE_M)

    def addText(self, txt, x, y, color=colors.NEGRO_F):
        window.blit(font_1.render(str(txt), True, color), (x, y))


class LogicBoard(object):
    def __init__(self, size, n_tank, tank_1, tank_2, tank_3=None, tank_4=None):
        self.size = size
        self.n_tank = n_tank
        self.tank_1 = tank_1
        self.tank_2 = tank_2
        self.tank_3 = tank_3
        self.tank_4 = tank_4
        self.tablero = self.generar_tablero()
        self.update_pos()
        self.dibujar_tablero()
        self.aux_x_t1 = -1
        self.aux_y_t1 = -1
        self.aux_x_t2 = -1
        self.aux_y_t2 = -1
        self.flag_mt1 = False
        self.flag_mt2 = False
        self.t1_m_id = 5
        self.t2_m_id = 10

    def update_pos(self):
        if self.n_tank == 2:
            self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
            self.tablero[self.tank_2.get_y()][self.tank_2.get_x()] = 2

    def generar_tablero(self):
        numero_filas, numero_columnas = self.size, self.size
        tablero = [0] * numero_filas
        for i in range(numero_filas):
            tablero[i] = [0] * numero_columnas
        return tablero

    def dibujar_tablero(self):
        for c in self.tablero:
            print(c)

    def mover_tanque(self, t_n, dir):
        if t_n == 1:
            if dir == "Este":
                if (self.tank_1.get_x() + 1) < self.size:
                    if self.tablero[self.tank_1.get_y()][self.tank_1.get_x() + 1] == 0:
                        # self.dibujar_tablero()
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x + 1, aux_y)
                        self.tank_1.posicion = pt
                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        return True
                    elif self.tablero[self.tank_1.get_y()][self.tank_1.get_x() + 1] > 5:
                        self.tank_1.mina_colisionada = self.tablero[self.tank_1.get_y()][self.tank_1.get_x() + 1]
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x + 1, aux_y)
                        self.tank_1.posicion = pt
                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        self.tank_1.reducir_vida(MINA_EXPLOTADO)
                        self.tank_1.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False
            elif dir == "Norte":
                if (self.tank_1.get_y() - 1) >= 0:
                    a = self.tank_1.get_y() - 1
                    print(a)
                    if self.tablero[self.tank_1.get_y() - 1][self.tank_1.get_x()] == 0:
                        # self.dibujar_tablero()
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x, aux_y - 1)
                        self.tank_1.posicion = pt
                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        return True
                    elif self.tablero[self.tank_1.get_y() - 1][self.tank_1.get_x()] > 5:
                        # self.dibujar_tablero()
                        self.tank_1.mina_colisionada = self.tablero[self.tank_1.get_y() - 1][self.tank_1.get_x()]
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x, aux_y - 1)
                        self.tank_1.posicion = pt
                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        self.tank_1.reducir_vida(MINA_EXPLOTADO)
                        self.tank_1.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False
            elif dir == "Sur":
                if (self.tank_1.get_y() + 1) < self.size:
                    if self.tablero[self.tank_1.get_y() + 1][self.tank_1.get_x()] == 0:
                        # self.dibujar_tablero()
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x, aux_y + 1)
                        self.tank_1.posicion = pt

                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        return True
                    elif self.tablero[self.tank_1.get_y() + 1][self.tank_1.get_x()] > 5:
                        self.tank_1.mina_colisionada = self.tablero[self.tank_1.get_y() + 1][self.tank_1.get_x()]
                        # self.dibujar_tablero()
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x, aux_y + 1)
                        self.tank_1.posicion = pt

                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        self.tank_1.reducir_vida(MINA_EXPLOTADO)
                        self.tank_1.colisiono = True
                        return True

                    else:
                        return False
                else:
                    return False
            elif dir == "Oeste":
                if (self.tank_1.get_x() - 1) >= 0:
                    if self.tablero[self.tank_1.get_y()][self.tank_1.get_x() - 1] == 0:
                        # self.dibujar_tablero()
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x - 1, aux_y)
                        self.tank_1.posicion = pt

                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        return True
                    elif self.tablero[self.tank_1.get_y()][self.tank_1.get_x() - 1] > 5:
                        self.tank_1.mina_colisionada = self.tablero[self.tank_1.get_y()][self.tank_1.get_x() - 1]
                        # self.dibujar_tablero()
                        aux_x = self.tank_1.get_x()
                        aux_y = self.tank_1.get_y()
                        pt = (aux_x - 1, aux_y)
                        self.tank_1.posicion = pt

                        self.tablero[self.tank_1.get_y()][self.tank_1.get_x()] = 1
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(1)
                        self.tank_1.reducir_vida(MINA_EXPLOTADO)
                        self.tank_1.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False

        # ==============================================================================================================
        if t_n == 2:
            if dir == "Este":
                if (self.tank_2.get_x() + 1) < self.size:
                    if self.tablero[self.tank_2.get_y()][self.tank_2.get_x() + 1] == 0 or \
                            self.tablero[self.tank_2.get_y()][self.tank_2.get_x() + 1] > 5:
                        ax_1 = self.tablero[self.tank_2.get_y()][self.tank_2.get_x() + 1]
                        ax = self.tablero[self.tank_2.get_y()][self.tank_2.get_x() + 1] > 5
                        # self.dibujar_tablero()
                        aux_x = self.tank_2.get_x()
                        aux_y = self.tank_2.get_y()
                        pt = (aux_x + 1, aux_y)
                        self.tank_2.posicion = pt
                        self.tablero[self.tank_2.get_y()][self.tank_2.get_x()] = 2
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(2)
                        if ax:
                            self.tank_2.mina_colisionada = ax_1
                            self.tank_2.reducir_vida(MINA_EXPLOTADO)
                            self.tank_2.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False
            elif dir == "Norte":
                if (self.tank_2.get_y() - 1) >= 0:
                    if self.tablero[self.tank_2.get_y() - 1][self.tank_2.get_x()] == 0 or \
                            self.tablero[self.tank_2.get_y() - 1][self.tank_2.get_x()] > 5:
                        # self.dibujar_tablero()
                        ax_1 = self.tablero[self.tank_2.get_y() - 1][self.tank_2.get_x()]
                        ax = self.tablero[self.tank_2.get_y() - 1][self.tank_2.get_x()] > 5
                        aux_x = self.tank_2.get_x()
                        aux_y = self.tank_2.get_y()
                        pt = (aux_x, aux_y - 1)
                        self.tank_2.posicion = pt
                        print(self.tank_2.get_x())
                        self.tablero[self.tank_2.get_y()][self.tank_2.get_x()] = 2
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(2)
                        if ax:
                            self.tank_2.mina_colisionada = ax_1
                            self.tank_2.reducir_vida(MINA_EXPLOTADO)
                            self.tank_2.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False
            elif dir == "Sur":
                if (self.tank_2.get_y() + 1) < self.size:
                    if self.tablero[self.tank_2.get_y() + 1][self.tank_2.get_x()] == 0 or \
                            self.tablero[self.tank_2.get_y() + 1][self.tank_2.get_x()] > 5:
                        # self.dibujar_tablero()
                        ax_1 = self.tablero[self.tank_2.get_y() + 1][self.tank_2.get_x()]
                        ax = self.tablero[self.tank_2.get_y() + 1][self.tank_2.get_x()] > 5
                        aux_x = self.tank_2.get_x()
                        aux_y = self.tank_2.get_y()
                        pt = (aux_x, aux_y + 1)
                        self.tank_2.posicion = pt

                        self.tablero[self.tank_2.get_y()][self.tank_2.get_x()] = 2
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(2)
                        if ax:
                            self.tank_2.mina_colisionada = ax_1
                            self.tank_2.reducir_vida(MINA_EXPLOTADO)
                            self.tank_2.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False
            elif dir == "Oeste":
                if (self.tank_2.get_x() - 1) >= 0:
                    if self.tablero[self.tank_2.get_y()][self.tank_2.get_x() - 1] == 0 or \
                            self.tablero[self.tank_2.get_y()][self.tank_2.get_x() - 1] > 5:
                        # self.dibujar_tablero()
                        ax_1 = self.tablero[self.tank_2.get_y()][self.tank_2.get_x() - 1]
                        ax = self.tablero[self.tank_2.get_y()][self.tank_2.get_x() - 1] > 5
                        aux_x = self.tank_2.get_x()
                        aux_y = self.tank_2.get_y()
                        pt = (aux_x - 1, aux_y)
                        self.tank_2.posicion = pt

                        self.tablero[self.tank_2.get_y()][self.tank_2.get_x()] = 2
                        self.tablero[aux_y][aux_x] = 0
                        self.activate_mina(2)
                        if ax:
                            self.tank_2.mina_colisionada = ax_1
                            self.tank_2.reducir_vida(MINA_EXPLOTADO)
                            self.tank_2.colisiono = True
                        return True
                    else:
                        return False
                else:
                    return False

    def activate_mina(self, t_n):
        if t_n == 1 and self.flag_mt1:
            self.t1_m_id += 1
            self.tablero[self.aux_y_t1][self.aux_x_t1] = self.t1_m_id
            self.flag_mt1 = False
        elif t_n == 2 and self.flag_mt2:
            self.t2_m_id += 1
            self.tablero[self.aux_y_t2][self.aux_x_t2] = self.t2_m_id
            self.flag_mt2 = False

    def get_uid_mina(self, t_n):
        if t_n == 1:
            return self.t1_m_id + 1
        elif t_n == 2:
            return self.t2_m_id + 1

    def config_mina(self, t_n):
        if t_n == 1:
            if self.tank_1.n_minas > 0:
                self.aux_x_t1 = self.tank_1.get_x()
                self.aux_y_t1 = self.tank_1.get_y()
                self.flag_mt1 = True
                self.tank_1.n_minas = self.tank_1.n_minas - 1
                return True
            else:
                return False
        elif t_n == 2:
            if self.tank_2.n_minas > 0:
                self.aux_x_t2 = self.tank_2.get_x()
                self.aux_y_t2 = self.tank_2.get_y()
                self.flag_mt2 = True
                self.tank_2.n_minas = self.tank_2.n_minas - 1
                return True
            else:
                return False

    def radar(self, dir, t_n):
        if t_n == 2:
            if dir == "Norte":
                ind = self.tank_2.get_y()
                ind_found = -1
                r = 0
                for r in range(ind - 1, -1, -1):
                    r += 1
                    if 0 < self.tablero[int(r)][self.tank_2.get_x()] < 5:
                        print("Jugador encontrado")
                        ind_found = r
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = (self.tank_2.get_y() * -1)
                print(ind_found)
                return ind_found
            elif dir == "Sur":
                ind = self.tank_2.get_y()
                ind_found = -1
                r = 0
                for r in range(ind + 1, self.size, 1):
                    print(r)
                    if 0 < self.tablero[int(r)][self.tank_2.get_x()] < 5:
                        print("Jugador encontrado")
                        ind_found = r
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = ((self.tank_2.get_y() + 1) - self.size)
                print(ind_found)
                return ind_found
            elif dir == "Este":
                ind = self.tank_2.get_x()
                ind_found = -1
                c = 0
                for r in range(ind + 1, self.size, 1):
                    c += 1
                    if 0 < self.tablero[self.tank_2.get_y()][r] < 5:
                        print("Jugador encontrado")
                        ind_found = c
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = ((self.tank_2.get_x() + 1) - self.size)
                print(ind_found)
                return ind_found
            elif dir == "Oeste":
                ind = self.tank_2.get_x()
                ind_found = -1
                r = 0
                for r in range(ind - 1, -1, -1):
                    r += 1
                    if 0 < self.tablero[self.tank_2.get_y()][r] < 5:
                        print("Jugador encontrado")
                        ind_found = r
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = (self.tank_2.get_x() * -1)
                print(ind_found)
                return ind_found
        if t_n == 1:
            if dir == "Norte":
                ind = self.tank_1.get_y()
                ind_found = -1
                r = 0
                for r in range(ind - 1, -1, -1):
                    r += 1
                    if 0 < self.tablero[int(r)][self.tank_1.get_x()] < 5:
                        print("Jugador encontrado")
                        ind_found = r
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = (self.tank_1.get_y() * -1)
                print(ind_found)
                return ind_found
            elif dir == "Sur":
                ind = self.tank_1.get_y()
                ind_found = -1
                r = 0
                for r in range(ind + 1, self.size, 1):
                    print(r)
                    if 0 < self.tablero[int(r)][self.tank_1.get_x()] < 5:
                        print("Jugador encontrado")
                        ind_found = r
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = ((self.tank_1.get_y() + 1) - self.size)
                print(ind_found)
                return ind_found
            elif dir == "Este":
                ind = self.tank_1.get_x()
                ind_found = -1
                c = 0
                for r in range(ind + 1, self.size, 1):
                    c += 1
                    if 0 < self.tablero[self.tank_1.get_y()][r] < 5:
                        print("Jugador encontrado")
                        ind_found = c
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = ((self.tank_1.get_x() + 1) - self.size)
                print(ind_found)
                return ind_found
            elif dir == "Oeste":
                ind = self.tank_1.get_x()
                ind_found = -1
                r = 0
                for r in range(ind - 1, -1, -1):
                    r += 1
                    if 0 < self.tablero[self.tank_1.get_y()][r] < 5:
                        print("Jugador encontrado")
                        ind_found = r
                        break
                if ind_found == -1:
                    print("RESULTADO DE RADAR")
                    ind_found = (self.tank_1.get_x() * -1)
                print(ind_found)
                return ind_found


class ExplosionSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, board_size):
        super(ExplosionSprite, self).__init__()
        self.b = Board(board_size)
        self.px = x
        self.py = y
        self.x = self.b.hi + 10 + 100 * x
        self.y = self.b.vi + 10 + 100 * y
        self.images = [pygame.image.load(img) for img in glob.glob("sprites/explosion\\*.png")]
        self.index = 0
        self.rect = pygame.Rect(self.x, self.y, 90, 90)
        self.update()

    def set_x(self, x):
        self.x = self.b.hi + 10 + 100 * x

    def set_y(self, y):
        self.y = self.b.vi + 10 + 100 * y

    def take_n_pos(self):
        self.rect = pygame.Rect(self.x, self.y, 90, 90)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1


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
        while p1 == p2:
            p1 = self.generar_pos(tablero)
            p2 = self.generar_pos(tablero)
        print("----------> tanque1: " + str(p1))

        t1 = tanques.Tank(1, "Rojo", 3, 10, p1)
        # tablero[t1.get_x()][t1.get_y()] = t1.nombre

        print("----------> tanque2: " + str(p2))
        t2 = tanques.Tank(2, "Rojo", 3, 10, p2)
        # tablero[t2.get_x()][t2.get_y()] = t2.nombre
        print("\n\n")
        # print(self.dibujar_tablero(tablero))

        # Definimos los sprites
        tank_1 = TankPlayer(p1[0], p1[1], self.tam_tablero, "sprites/tanque1\\*.png")
        tank_2 = TankPlayer(p2[0], p2[1], self.tam_tablero, "sprites/tanque2\\*.png")

        exp_1 = ExplosionSprite(-10, -10, self.tam_tablero)

        g1 = pygame.sprite.Group(tank_1)
        g2 = pygame.sprite.Group(tank_2)
        ge = pygame.sprite.Group(exp_1)
        # Definimos el tablero logico
        print("----------------------------------------")
        lb = LogicBoard(self.tam_tablero, 2, t1, t2)
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
        pygame.time.set_timer(pygame.USEREVENT + 2, 2500)  # Detenido temporalmente 2500
        flag = False
        m = []
        mina = Mina(-1, -10, -10, self.tam_tablero)
        m.append(mina)
        m2 = []
        mina = Mina(-1, -10, -10, self.tam_tablero)
        m2.append(mina)
        mina.set_visible(False)
        mt1 = False
        mt2 = False
        radar_px_1 = 0
        radar_px_2 = 0
        while not stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == (pygame.USEREVENT + 2):
                    nom_tanque = next(pool_tanques).nombre
                    if nom_tanque == 1:
                        i1 = next(pool_t1)
                        # print("Tanque 1: " + i1)
                        st.ins_exe = "Tanque 1: " + i1
                        pygame.time.set_timer(pygame.USEREVENT + 4, 0)
                        pygame.time.set_timer(pygame.USEREVENT + 7, 0)
                        # pygame.time.set_timer(pygame.USEREVENT + 6, 0)
                        if i1 == "mover(E)" and lb.mover_tanque(1, "Este"):
                            pygame.time.set_timer(pygame.USEREVENT + 3, 120)
                        elif i1 == "mover(N)" and lb.mover_tanque(1, "Norte"):
                            pygame.time.set_timer(pygame.USEREVENT + 3, 120)
                        elif i1 == "mover(S)" and lb.mover_tanque(1, "Sur"):
                            pygame.time.set_timer(pygame.USEREVENT + 3, 120)
                        elif i1 == "mover(O)" and lb.mover_tanque(1, "Oeste"):
                            pygame.time.set_timer(pygame.USEREVENT + 3, 120)
                        elif i1 == "radar(N)":
                            radar_px_1 = lb.radar("Norte", 1)
                        elif i1 == "radar(S)":
                            radar_px_1 = lb.radar("Sur", 1)
                        elif i1 == "radar(E)":
                            radar_px_1 = lb.radar("Este", 1)
                        elif i1 == "radar(O)":
                            radar_px_1 = lb.radar("Oeste", 1)
                        elif i1 == "mina()" and lb.config_mina(1):
                            mt1 = True
                            print("Mina a guardar: " + str(lb.get_uid_mina(1)))
                            m2.append(Mina(lb.get_uid_mina(1), t1.get_x(), t1.get_y(), self.tam_tablero))

                        if t1.colisiono:
                            # Botamos la mina y escondemos la original
                            # Datos guardados
                            for i in m2:
                                print(i.id)
                            mqe = t1.mina_colisionada
                            print("---------------------------------------1> " + str(mqe))
                            indice = 0
                            for i in m2:
                                print(i.id)
                                if mqe == i.id:
                                    break
                                indice += 1
                            print("Indice : ---> " + str(indice))
                            if indice is not 0:
                                m2.pop(indice)
                            # m[-1].set_visible(True)
                            # Generamos explosion
                            pygame.time.set_timer(pygame.USEREVENT + 6, 300)
                            t1.colisiono = False

                        print("\n")
                        lb.dibujar_tablero()
                        # time.sleep(1)
                    elif nom_tanque == 2:
                        i2 = next(pool_t2)
                        # print("Tanque 2: " + i2)
                        st.ins_exe = "Tanque 2: " + i2
                        pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                        # Ocultar explosion tanque 1 desde tanque 2
                        pygame.time.set_timer(pygame.USEREVENT + 6, 0)
                        exp_1.set_x(-10)
                        exp_1.set_y(-10)
                        exp_1.take_n_pos()
                        if i2 == "mover(E)" and lb.mover_tanque(2, "Este"):
                            pygame.time.set_timer(pygame.USEREVENT + 4, 120)
                        elif i2 == "mover(N)" and lb.mover_tanque(2, "Norte"):
                            pygame.time.set_timer(pygame.USEREVENT + 4, 120)
                        elif i2 == "mover(S)" and lb.mover_tanque(2, "Sur"):
                            pygame.time.set_timer(pygame.USEREVENT + 4, 120)
                        elif i2 == "mover(O)" and lb.mover_tanque(2, "Oeste"):
                            pygame.time.set_timer(pygame.USEREVENT + 4, 120)
                        elif i2 == "radar(N)":
                            radar_px_2 = lb.radar("Norte", 2)
                        elif i2 == "radar(S)":
                            radar_px_2 = lb.radar("Sur", 2)
                        elif i2 == "radar(E)":
                            radar_px_2 = lb.radar("Este", 2)
                        elif i2 == "radar(O)":
                            radar_px_2 = lb.radar("Oeste", 2)
                        elif i2 == "mina()" and lb.config_mina(2):
                            mt2 = True
                            print("Mina a guardar" + str(lb.get_uid_mina(2)))
                            m2.append(Mina(lb.get_uid_mina(2), t2.get_x(), t2.get_y(), self.tam_tablero))
                        if t2.colisiono:
                            # Botamos la mina y escondemos la original
                            # Datos guardados
                            for i in m2:
                                print(i.id)
                            mqe = t2.mina_colisionada
                            print("---------------------------------------2> " + str(mqe))
                            indice = 0
                            for i in m2:
                                print(i.id)
                                if mqe == i.id:
                                    break
                                indice += 1
                            print("Indice : ---> " + str(indice))
                            if indice is not 0:
                                m2.pop(indice)
                            # Generamos explosion
                            pygame.time.set_timer(pygame.USEREVENT + 7, 300)
                            t2.colisiono = False
                        print("\n")
                        lb.dibujar_tablero()
                        # time.sleep(1)
                elif event.type == (pygame.USEREVENT + 3):
                    # Se supone que aqui iran las instrucciones del tanque 1
                    if mt1:
                        mt1 = False
                        pygame.time.set_timer(pygame.USEREVENT + 5, 1)
                    if i1 == "mover(E)":
                        tank_1.move("Este")
                        g1.update(0)
                    elif i1 == "mover(N)":
                        tank_1.move("Norte")
                        g1.update(90)
                    elif i1 == "mover(S)":
                        tank_1.move("Sur")
                        g1.update(270)
                    elif i1 == "mover(O)":
                        tank_1.move("Oeste")
                        g1.update(180)
                elif event.type == (pygame.USEREVENT + 4):
                    if mt2:
                        mt2 = False
                        pygame.time.set_timer(pygame.USEREVENT + 5, 1)
                    if i2 == "mover(E)":
                        tank_2.move("Este")
                        g2.update(0)
                    elif i2 == "mover(N)":
                        tank_2.move("Norte")
                        g2.update(90)
                    elif i2 == "mover(S)":
                        tank_2.move("Sur")
                        g2.update(270)
                    elif i2 == "mover(O)":
                        tank_2.move("Oeste")
                        g2.update(180)
                elif event.type == (pygame.USEREVENT + 5):
                    for o in m2:
                        o.set_visible(True)

                elif event.type == (pygame.USEREVENT + 6):
                    # print("Hola desde el evento 6")
                    exp_1.set_x(t1.get_x())
                    exp_1.set_y(t1.get_y())
                    exp_1.take_n_pos()
                    ge.update()

                elif event.type == (pygame.USEREVENT + 7):
                    exp_1.set_x(t2.get_x())
                    exp_1.set_y(t2.get_y())
                    exp_1.take_n_pos()
                    ge.update()

            window.fill(colors.BCK_COLOR)
            board.draw()
            st.draw()
            st.minas_j1_data = str(t1.n_minas)
            st.minas_j2_data = str(t2.n_minas)
            st.player_1_life = str(t1.vida) + "%"
            st.player_2_life = str(t2.vida) + "%"
            st.px1_data = str(radar_px_1)
            st.px2_data = str(radar_px_2)
            for pp in m2:
                pp.draw()
            g1.draw(window)
            g2.draw(window)
            ge.draw(window)

            pygame.display.flip()
            pygame.display.update()
            window_clock.tick(60)


if __name__ == "__main__":
    MainRun(display_w, display_h, 6)
