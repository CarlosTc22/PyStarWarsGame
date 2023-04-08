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
        ruta = os.path.join("resources", "images", "Portada_oscura.png")
        self.portada = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 60)

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True
            self.pintar_portada()
            self.pintar_texto()
            pg.display.flip()

    def pintar_portada(self):
        self.pantalla.blit(self.portada, (0, 0))

    def pintar_texto(self):
        mensaje = "Pulsa espacio para comenzar la partida"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO/4 
        self.pantalla.blit(texto, ( pos_x, pos_y))



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