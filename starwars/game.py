import os
import pygame as pg
from . import ALTO, ANCHO
from .escenas import Portada, Tutorial, Nivel_Facil, Nivel_Dificil, Records

class Starwars:

    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption("Star Wars")

        ruta = os.path.join("resources", "images", "icono.png")
        icon = pg.image.load(ruta)
        pg.display.set_icon(icon)

        self.escenas = [
            Portada(self.pantalla),
            Tutorial(self.pantalla),
            "Nivel_Facil(self.pantalla), Nivel_Dificil(self.pantalla), Records(self.pantalla)"

            ]


    def jugar (self):
        "Bucle principal"
        for escena in self.escenas:
            escena.bucle_principal()