import os
import pygame as pg
from . import ALTO, ANCHO
from .escenas import Portada, Tutorial, Nivel_Facil, Nivel_Dificil, Records, Historia

class Starwars:

    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption("Star Wars")

        ruta = os.path.join("resources", "images", "icono.png")
        icon = pg.image.load(ruta)
        pg.display.set_icon(icon)

        self.escenas = {
            "portada": Portada(self.pantalla),
            "tutorial": Tutorial(self.pantalla),
            "historia": Historia(self.pantalla),
            "records": Records(self.pantalla),
            "nivel_facil": Nivel_Facil(self.pantalla),
            "nivel_dificil": Nivel_Dificil(self.pantalla),
        }
        self.escena_actual = "portada"


    def jugar(self):
        "Bucle principal"
        vidas_restantes = 3 
        puntuacion_obtenida = 0

        while self.escena_actual is not None:
            resultado = self.escenas[self.escena_actual].bucle_principal()
            if resultado == "game_over":
                puntuacion_obtenida = self.escenas["nivel_facil"].puntuacion 
                self.escenas["records"] = Records(self.pantalla, 10, puntuacion_obtenida) 
                self.escena_actual = "records"
            elif resultado == "continue":
                vidas_restantes = self.escenas["nivel_facil"].vidas 
                puntuacion_obtenida = self.escenas["nivel_facil"].puntuacion 
                self.escenas["nivel_dificil"] = Nivel_Dificil(self.pantalla, vidas_restantes, puntuacion_obtenida) 
                self.escena_actual = "nivel_dificil"
            else:
                self.escena_actual = resultado