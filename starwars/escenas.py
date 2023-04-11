import os
import random
import pygame as pg
from . import ALTO, ANCHO
from .assets import Ball_Training, Laser, Meteorito, X_Wing 

class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla

    def bucle_principal(self):
        pass

class Portada(Escena):

    # Se pone el fondo de la portada y los mensajes de texto

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
                    return "salir"
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return "nivel_facil"
                if event.type == pg.KEYDOWN and event.key == pg.K_t:
                    return "tutorial"
                if event.type == pg.KEYDOWN and event.key == pg.K_h:
                    return "historia"
                if event.type == pg.KEYDOWN and event.key == pg.K_r:
                    return "records"
            self.pintar_portada()
            self.pintar_texto()
            self.pintar_textotutorial()
            pg.display.flip()
        return False


    def pintar_portada(self):
        self.pantalla.blit(self.portada, (0, 0))

    def pintar_texto(self):
        mensaje = "Pulsa espacio para comenzar la partida"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO/4 
        self.pantalla.blit(texto, ( pos_x, pos_y))
   
    def pintar_textotutorial(self):
        mensaje = "Si hacer el tutorial quieres, T debes pulsar"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO* 3/4 
        self.pantalla.blit(texto, ( pos_x, pos_y))




class Tutorial(Escena):

    # Escena del tutorial, sin daño.

    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 30)
        self.x_wing = X_Wing()
        self.ball_training = Ball_Training()
        
        # Se crea una lista para almacenar los disparos y se define un temporizador

        self.lasers = []  
        self.laser_timer = pg.USEREVENT + 1  
        pg.time.set_timer(self.laser_timer, 1000)  

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    return "portada"
        # Si se produce el evento de temporizador, se añade un láser a la lista
                elif event.type == self.laser_timer:  
                    self.lasers.append(Laser())  
            self.pintar_fondo()
            self.x_wing.update()
        # Se actualiza la posición de los láseres y se pintan
            for laser in self.lasers:  
                laser.update()
                self.pantalla.blit(laser.image, laser.rect)

            self.pantalla.blit(self.x_wing.image, self.x_wing.rect)
            self.ball_training.update()
        # Se actualiza la posición de Ball_Training y se pinta
            self.pantalla.blit(self.ball_training.image, self.ball_training.rect)
            self.pintar_instrucciones()
            pg.display.flip()
        return False

    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_instrucciones(self):
        mensaje = "Muevete arriba y abajo para esquivar los disparos"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO* 3/4 
        self.pantalla.blit(texto, ( pos_x, pos_y))

        mensaje2 = "Aquí no hacen daño"
        texto2 = self.font.render(mensaje2, True, (255, 255, 255))
        pos_x2 = ANCHO/2 - texto2.get_width()/2
        pos_y2 = ALTO* .80 
        self.pantalla.blit(texto2, ( pos_x2, pos_y2))


class Nivel_Facil(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 30)

        self.x_wing = X_Wing()
        self.meteoritos = []
        self.meteoritos_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.meteoritos_timer, 500)
        self.vidas = 3
        self.pausa_meteoritos = False
        self.timer_pausa = pg.USEREVENT + 2
        self.timer_nivel = pg.USEREVENT + 3
        pg.time.set_timer(self.timer_nivel, 20000)
        self.puntuacion = 0
        self.tiempotranscurrido_timer = 0
        self.start_time = pg.time.get_ticks()

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                elif self.vidas <= 0:
                    self.puntuacion = self.vidas
                    return ("game_over")
                elif event.type == self.meteoritos_timer and not self.pausa_meteoritos:
                    self.meteoritos.append(Meteorito())
                elif event.type == self.timer_pausa:
                    self.x_wing.rect.y = ALTO/2                  
                    self.pausa_meteoritos = False
                    pg.time.set_timer(self.timer_pausa, 0)
                elif event.type == self.timer_nivel:
                    self.puntuacion = self.vidas
                    return ("continue")
                
            self.tiempotranscurrido_timer = pg.time.get_ticks() - self.start_time
            self.pintar_fondo()
            self.pintar_temporizador()
            self.x_wing.update()
            self.x_wing.detectar_colision(self)

            if self.x_wing.hay_colision:
                self.vidas -= 1
                self.x_wing.hay_colision = False
                self.pausa_meteoritos = True
                self.x_wing.rect.y = -5 * ALTO
                pg.time.set_timer(self.timer_pausa, 3000)


            for meteorito in self.meteoritos:
                meteorito.update()
                self.pantalla.blit(meteorito.image, meteorito.rect)

            self.pantalla.blit(self.x_wing.image, self.x_wing.rect)
            self.mostrar_vidas()
            pg.display.flip()

        return False

    def mostrar_vidas(self):
        texto = self.font.render(f"vidas: {self.vidas}", True, (255, 255, 255))
        self.pantalla.blit(texto, (50, 50))

    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_temporizador(self):
        tiempo_restante = 20 - (self.tiempotranscurrido_timer // 1000)  
        texto = self.font.render(f"{tiempo_restante}", True, (255, 255, 255))
        self.pantalla.blit(texto, (ANCHO - texto.get_width() - 50, 50))

class Nivel_Dificil(Nivel_Facil):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)

        self.meteoritos_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.meteoritos_timer, 400)  # Aumentamos la frecuencia de aparición de los láseres
        self.timer_nivel = pg.USEREVENT + 3
        pg.time.set_timer(self.timer_nivel, 25000)  # Aumentamos el tiempo del nivel a 25 segundos
        self.start_time = pg.time.get_ticks()
        
    def bucle_principal(self):
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                elif self.vidas <= 0:
                    self.puntuacion = self.vidas
                    return "game_over"
                elif event.type == self.meteoritos_timer and not self.pausa_meteoritos:
                    self.meteoritos.append(Meteorito())  # Cambiamos Meteorito por Laser
                # ... (otros eventos)
                elif event.type == self.timer_nivel:
                    return "portada"  # En lugar de "continue", regresamos a la portada

            self.tiempotranscurrido_timer = pg.time.get_ticks() - self.start_time
            self.pintar_fondo()
            self.pintar_temporizador()
            self.x_wing.update()
            self.x_wing.detectar_colision(self)

            if self.x_wing.hay_colision:
                self.vidas -= 1
                self.x_wing.hay_colision = False
                self.pausa_meteoritos = True
                self.x_wing.rect.y = -5 * ALTO
                pg.time.set_timer(self.timer_pausa, 3000)

            for meteorito in self.meteoritos:
                meteorito.update()
                self.pantalla.blit(meteorito.image, meteorito.rect)

            self.pantalla.blit(self.x_wing.image, self.x_wing.rect)
            self.mostrar_vidas()
            pg.display.flip()

        return False

class Records(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 60)

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True
            self.pintar_fondo()
            pg.display.flip()
        return False
    
    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))

class Historia(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)