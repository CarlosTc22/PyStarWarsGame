import os
import pygame as pg
from . import ALTO, ANCHO

class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla

    def bucle_principal(self):
        pass

class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "Portada.jpg")
        self.portada = pg.image.load(ruta)


    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True
            self.pintar_portada()
            pg.display.flip()

    def pintar_portada(self):
        self.pantalla.blit(self.portada, (0, 0))


class Tutorial(Escena):
    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pantalla.fill((100, 0 ,100))
            pg.display.flip()

class Nivel_Facil(Escena):
    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pantalla.fill((100, 100 ,0))
            pg.display.flip()

class Nivel_Dificil(Escena):
    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pantalla.fill((0, 100 ,0))
            pg.display.flip()

class Records(Escena):
    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pantalla.fill((0, 0 ,100))
            pg.display.flip()