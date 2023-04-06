import pygame as pg
from starwars import ALTO, ANCHO


class Starwars:

    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))

    def jugar (self):
        "Bucle principal"
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pantalla.fill((100, 0 ,0))
            pg.display.flip()
            