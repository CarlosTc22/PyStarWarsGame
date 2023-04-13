import os
import pygame as pg
from . import ALTO, ANCHO, METEORITOS_NIVEL_DIFICIL, METEORITOS_NIVEL_FACIL
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
    def __init__(self, pantalla, vidas=3, puntuacion=0):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 30)

        self.x_wing = X_Wing()
        self.meteoritos = []
        self.duracion_nivel = 20
        self.vidas = vidas
        self.pausa_meteoritos = False
        self.timer_pausa = pg.USEREVENT + 1
        self.timer_nivel = pg.USEREVENT + 2
        self.puntuacion = puntuacion
        self.tiempotranscurrido_timer = 0
        self.start_time = pg.time.get_ticks()
        self.cruzado_eje_x = False
        self.mostrar_marcadores = True
        self.espera_timer = pg.USEREVENT + 3
        self.pausa_final = False
        self.contador_meteoritos = 0
        self.limite_meteoritos = METEORITOS_NIVEL_FACIL

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        espera_iniciada = False
        while not salir:
            self.tiempotranscurrido_timer = pg.time.get_ticks() - self.start_time
            tiempo_restante = self.duracion_nivel - (self.tiempotranscurrido_timer // 1000)

            if tiempo_restante <= 0 and not espera_iniciada:
                self.mostrar_marcadores = False
                self.pausa_final = True
                pg.time.set_timer(self.espera_timer, 5000)
                espera_iniciada = True

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"  
                
                elif self.vidas <= 0:
                    print("game_over")
                    return ("game_over")
                elif not self.pausa_meteoritos and not self.pausa_final:
                    if self.contador_meteoritos < self.limite_meteoritos:
                        self.meteoritos.append(Meteorito())
                        self.contador_meteoritos += 1
                elif event.type == self.timer_pausa:
                    self.x_wing.rect.y = ALTO/2                  
                    self.pausa_meteoritos = False
                    pg.time.set_timer(self.timer_pausa, 0)
                elif event.type == self.espera_timer:
                    print("continue")
                    return ("continue")

            self.tiempotranscurrido_timer = pg.time.get_ticks() - self.start_time
            self.pintar_fondo()
            self.x_wing.update()
            self.x_wing.detectar_colision(self)

            if self.x_wing.hay_colision:
                self.vidas -= 1
                self.x_wing.hay_colision = False
                self.pausa_meteoritos = True
                self.x_wing.rect.y = -5 * ALTO
                pg.time.set_timer(self.timer_pausa, 5000)

            for meteorito in self.meteoritos:
                meteorito.update()
                self.pantalla.blit(meteorito.image, meteorito.rect)
                if meteorito.rect.x <= 0 and not meteorito.cruzado_eje_x:
                    self.puntuacion += 10
                    meteorito.cruzado_eje_x = True

            self.pantalla.blit(self.x_wing.image, self.x_wing.rect)
            if self.mostrar_marcadores:
                self.mostrar_vidas()
                self.mostrar_puntuacion()
                self.pintar_temporizador()
            pg.display.flip()

        return False

    def mostrar_vidas(self):
        texto = self.font.render(f"vidas: {self.vidas}", True, (255, 255, 255))
        self.pantalla.blit(texto, (50, 50))

    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_temporizador(self):
        tiempo_restante = self.duracion_nivel - (self.tiempotranscurrido_timer // 1000)  
        texto = self.font.render(f"{tiempo_restante}", True, (255, 255, 255))
        self.pantalla.blit(texto, (ANCHO - texto.get_width() - 50, 50))
    
    def mostrar_puntuacion(self):
        texto = self.font.render(f"puntuación: {self.puntuacion}", True, (255, 255, 255))
        self.pantalla.blit(texto, (50, 100))

class Nivel_Dificil(Nivel_Facil):
    def __init__(self, pantalla, vidas=3, puntuacion = 0): 
        super().__init__(pantalla, vidas, puntuacion)
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)
        self.duracion_nivel = 25
        self.espera_timer = pg.USEREVENT + 4
        self.limite_meteoritos = METEORITOS_NIVEL_DIFICIL
        self.contador_meteoritos = 0


    def bucle_principal(self):
        resultado = super().bucle_principal()
        
        if resultado == "continue":
            print ("fallo")
            return "portada"
        
        return resultado

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