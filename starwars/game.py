import pygame as pg
from starwars import ALTO, ANCHO
from starwars.escenas import Portada, Tutorial, Nivel_Facil, Nivel_Dificil, Records

class Starwars:

    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))

        self.escenas = [
            Portada(self.pantalla),
            Tutorial(self.pantalla),
            Nivel_Facil(self.pantalla),
            Nivel_Dificil(self.pantalla),
            Records(self.pantalla)

            ]


    def jugar (self):
        "Bucle principal"
        for escena in self.escenas:
            escena.bucle_principal()