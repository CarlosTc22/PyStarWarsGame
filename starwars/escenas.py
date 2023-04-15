import os
import pygame as pg
from pygame.locals import *
from . import ALTO, ANCHO, METEORITOS_NIVEL_DIFICIL, METEORITOS_NIVEL_FACIL
from .assets import Ball_Training, Explosion, Laser, Meteorito, Planeta, X_Wing 
from .records import recuperar_records, agregar_record

class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        ruta = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 30)


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
                    return "game_over"
            self.pintar_portada()
            self.pintar_texto()
            self.pintar_textotutorial()
            pg.display.flip()
        return False


    def pintar_portada(self):
        self.pantalla.blit(self.portada, (0, 0))

    def pintar_texto(self):
        mensaje = "Pulsa espacio para comenzar la partida"
        mensaje2 = "Pulsa H para conocer la historia"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        texto2 = self.font.render(mensaje2, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO * 0.20 
        self.pantalla.blit(texto, ( pos_x, pos_y))
        pos_x2 = ANCHO/2 - texto.get_width()/2
        pos_y2 = ALTO * .30
        self.pantalla.blit(texto2, ( pos_x2, pos_y2))
    def pintar_textotutorial(self):
        mensaje = "Si hacer el tutorial quieres, T debes pulsar"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO* 0.60 
        self.pantalla.blit(texto, ( pos_x, pos_y))
        mensaje2 = "Con R a los records entrarás"
        texto2 = self.font.render(mensaje2, True, (255, 255, 255))
        pos_x2 = ANCHO/2 - texto.get_width()/2
        pos_y2 = ALTO * 0.70 
        self.pantalla.blit(texto2, ( pos_x2, pos_y2))

class Tutorial(Escena):

    # Escena del tutorial, sin daño.

    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background2.png")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 30)
        self.x_wing = X_Wing()
        self.ball_training = Ball_Training()
        
        # Se crea una lista para almacenar los disparos y se define un temporizador

        self.lasers = []  
        self.laser_timer = pg.USEREVENT + 10  
        pg.time.set_timer(self.laser_timer, 1000)  

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
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

        mensaje2 = "Aquí no hacen daño, pulsa espacio para continuar"
        texto2 = self.font.render(mensaje2, True, (255, 255, 255))
        pos_x2 = ANCHO/2 - texto2.get_width()/2
        pos_y2 = ALTO* .80 
        self.pantalla.blit(texto2, ( pos_x2, pos_y2))

class Nivel_Facil(Escena):
    # Se utilizan los eventos de pg para gestionar los eventos del juego
    def __init__(self, pantalla, vidas = 3, puntuacion = 0):
        super().__init__(pantalla)
        self.x_wing = X_Wing()
        self.meteoritos = []
        self.vidas = vidas
        self.pausa_meteoritos = False
        self.timer_pausa = pg.USEREVENT + 1
        self.puntuacion = puntuacion
        self.cruzado_eje_x = False
        self.mostrar_marcadores = True
        self.espera_timer = pg.USEREVENT + 3
        self.pausa_final = False
        self.contador_meteoritos = 0
        self.limite_meteoritos = METEORITOS_NIVEL_FACIL # Dificultad del nivel
        self.mover_nave_activado = False
        self.mostrar_texto = False
        self.planeta = Planeta()
        self.angulo = 0
        self.rotacion = False
        self.fin_rotacion = False
        self.explosion_group = pg.sprite.Group()
        self.contador_meteoritos_puntuacion = 0

    def bucle_principal(self):
        salir = False
        espera_iniciada = False
        while not salir:
         # Condicion para acabar el nivel:       
            if self.contador_meteoritos_puntuacion >= self.limite_meteoritos and not espera_iniciada:
                self.mostrar_marcadores = False
                self.pausa_final = True
                pg.time.set_timer(self.espera_timer, 5000)
                espera_iniciada = True
                
        # Bucle gestor de los eventos:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"  
                
                elif self.vidas <= 0:
                    print("game_over")
                    self.iniciales = self.pedir_iniciales()
                    if self.iniciales != "salir":
                        agregar_record(self.iniciales, self.puntuacion)
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
                    self.mover_nave_activado = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.mostrar_texto:
                    print("continue")
                    return "continue"

                    
            self.pintar_fondo()
            self.x_wing.update()
            self.x_wing.detectar_colision(self)

            if self.mover_nave_activado:
                self.mover_nave()
                self.planeta.update()

            if self.mostrar_texto:
                self.pintar_texto()

        # Condición de colision con un meteorito:

            if self.x_wing.hay_colision:
                y = self.x_wing.rect.y
                explosion = Explosion(self.x_wing.rect.x, y)
                self.explosion_group.add(explosion)
                self.vidas -= 1
                self.x_wing.hay_colision = False
                self.pausa_meteoritos = True
                self.x_wing.rect.y = -5 * self.x_wing.rect.y
                pg.time.set_timer(self.timer_pausa, 5000)

        # Gestión de la lista de meteoritos, puntuación y fin del nivel:

            for meteorito in self.meteoritos:
                meteorito.update()
                self.pantalla.blit(meteorito.image, meteorito.rect)
                if meteorito.rect.x <= 0 and not meteorito.cruzado_eje_x:
                    if self.x_wing.rect.y > 0:
                        meteorito.cruzado_eje_x = True
                        self.contador_meteoritos_puntuacion += 1
                        self.puntuacion += 10
                    meteorito.cruzado_eje_x = True
            self.pantalla.blit(self.planeta.image, self.planeta.rect)

        # Condiciones para pintar elementos en pantalla o no pintarlos:

            if not self.mostrar_texto:
                self.pantalla.blit(self.x_wing.image, self.x_wing.rect)
            if self.mostrar_marcadores:
                self.mostrar_vidas()
                self.mostrar_puntuacion()

        # Pintar sprite de explosión:

            self.explosion_group.update()
            self.explosion_group.draw(self.pantalla)
            pg.display.flip()

        return False

    def mostrar_vidas(self): # Marcador de vidas
        texto = self.font.render(f"vidas: {self.vidas}", True, (255, 255, 255))
        self.pantalla.blit(texto, (50, 50))

    def pintar_fondo(self): 
        self.pantalla.blit(self.fondo, (0, 0))
    
    def mostrar_puntuacion(self): # Marcador de puntuación
        texto = self.font.render(f"puntuación: {self.puntuacion}", True, (255, 255, 255))
        self.pantalla.blit(texto, (50, 100))

    def mover_nave(self): # Aterrizaje de la nave
        i = 1
        destino_x = ANCHO - 600
        destino_y = ALTO / 2

        distancia_x = destino_x - self.x_wing.rect.x
        distancia_y = destino_y - self.x_wing.rect.y

        pasos = max(abs(distancia_x), abs(distancia_y))

        if pasos != 0:
            velocidad_x = distancia_x / pasos
            velocidad_y = distancia_y / pasos
        else:
            velocidad_x = 0
            velocidad_y = 0

        self.x_wing.rect.x += velocidad_x *3
        self.x_wing.rect.y += velocidad_y

        if abs(self.x_wing.rect.x - destino_x) < 1 and abs(self.x_wing.rect.y - destino_y) < 1:
            if self.angulo < 180:
                self.angulo += 2
                img_rotada = pg.transform.rotate(self.x_wing.image, self.angulo)
                rect_rotado = img_rotada.get_rect(center=self.x_wing.rect.center)
                self.pantalla.blit(img_rotada, rect_rotado)
            else:
                self.rotacion = False
                self.fin_rotacion = True
                img_rotada2 = pg.transform.rotate(self.x_wing.image, 180)
                rect_rotado2 = img_rotada2.get_rect(center=self.x_wing.rect.center)
                self.pantalla.blit(img_rotada2, rect_rotado2)

                
            self.mostrar_texto = True
        
    def pintar_texto(self): # Texto cuando la nave termina de aterrizar
        if self.mostrar_texto:
            mensaje = "Pulsa espacio para continuar"
            texto = self.font.render(mensaje, True, (255, 255, 255))
            pos_x = ANCHO/2 - texto.get_width()/2
            pos_y = ALTO* 3/4 
            self.pantalla.blit(texto, ( pos_x, pos_y))

    def pedir_iniciales(self): # Pide las iniciales para guardar un record
        iniciales = ""
        salir = False

        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                elif event.type == pg.KEYDOWN:
                    if event.unicode.isalpha() and len(iniciales) < 3:
                        iniciales += event.unicode.upper()
                    elif event.key == pg.K_BACKSPACE and len(iniciales) > 0:
                        iniciales = iniciales[:-1]
                    elif event.key == pg.K_SPACE and len(iniciales) == 3:
                        return iniciales

            self.pintar_fondo()

            mensaje = "ingrese sus iniciales: " + iniciales
            texto = self.font.render(mensaje, True, (255, 255, 255))
            pos_x = ANCHO / 2 - texto.get_width() / 2
            pos_y = ALTO / 2 - texto.get_height() / 2
            self.pantalla.blit(texto, (pos_x, pos_y))
            mensaje2 = "Pulsa espacio para continuar"
            texto = self.font.render(mensaje2, True, (255, 255, 255))
            pos_x2 = ANCHO / 2 - texto.get_width() / 2
            pos_y2 = ALTO * 0.60 - texto.get_height() / 2
            self.pantalla.blit(texto, (pos_x2, pos_y2))
            
            pg.display.flip()

class Nivel_Dificil(Nivel_Facil): # hereda casi todo de nivel facil, hay una modificación para aumentar la dificultad
    def __init__(self, pantalla, vidas=3, puntuacion = 0): 
        super().__init__(pantalla, vidas, puntuacion)
        self.espera_timer = pg.USEREVENT + 4
        self.limite_meteoritos = METEORITOS_NIVEL_DIFICIL # Dificultad del nivel
        self.contador_meteoritos = 0


    def bucle_principal(self):
        resultado = super().bucle_principal()
        
        if resultado == "continue":
            agregar_record(self.pedir_iniciales(), self.puntuacion)
            return ("game_over")
        
        return resultado

class Records(Nivel_Facil):
    def __init__(self, pantalla, vidas=3, puntuacion=0):
        super().__init__(pantalla, vidas, puntuacion)
        ruta = os.path.join("resources", "images", "background3.png")
        self.fondo = pg.image.load(ruta)
        self.records = recuperar_records() # Recupera los records de la base de datos

    def pintar_records(self):
        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 60)
        espacio_vertical = 80
        margen_izquierdo = 150
        margen_superior = 100

        mensaje = "Pulsa espacio para continuar"
        texto = self.font.render(mensaje, True, (255, 255, 255))
        pos_x = ANCHO/2 - texto.get_width()/2
        pos_y = ALTO* 0.60 
        self.pantalla.blit(texto, ( pos_x, pos_y))

        # Pintar encabezados de las columnas
        encabezado_nombre = self.font.render("Nombre", True, (255, 255, 255))
        encabezado_record = self.font.render("Record", True, (255, 255, 255))
        self.pantalla.blit(encabezado_nombre, (margen_izquierdo, margen_superior))
        self.pantalla.blit(encabezado_record, (ANCHO // 2 + margen_izquierdo, margen_superior))

        # Pintar la lista de récords
        for index, record in enumerate(self.records):
            texto_nombre = self.font.render(record["nombre"], True, (255, 255, 255))
            texto_record = self.font.render(str(record["record"]), True, (255, 255, 255))

            y = margen_superior + espacio_vertical * (index + 1)
            self.pantalla.blit(texto_nombre, (margen_izquierdo, y))
            self.pantalla.blit(texto_record, (ANCHO // 2 + margen_izquierdo, y))

            if index >= 5:
                break
            
    def bucle_principal(self):
        salir = False
        while not salir:
            self.pintar_fondo()
            self.pintar_records()
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return "portada"
                

class Historia(Escena):

    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images", "background4.png")
        self.fondo = pg.image.load(ruta)

        ruta_font = os.path.join("resources", "fonts", "Starjedi.ttf")
        self.font = pg.font.Font(ruta_font, 30)
        self.font_grande = pg.font.Font(ruta_font, 80)


    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "salir"
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return "portada"
            self.pintar_fondo()
            self.pintar_historia()
            pg.display.flip()
        return False

    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_historia(self):
        titulo = "En una galaxia muy lejana"
        texto = self.font_grande.render(titulo, True, (255,255,255))
        ancho_texto = texto.get_width()
        pos_x = (ANCHO - ancho_texto)//2
        pos_y = ALTO/8
        self.pantalla.blit(texto, (pos_x, pos_y))
        posiciones = [ALTO/4, ALTO/4 + 50, ALTO/4 + 100, ALTO/4 + 150, ALTO/4 + 200, ALTO/4 + 250, ALTO/4 + 300]
        mensajes = ["la Princesa Leia lidera una rebelión contra el Imperio Galáctico",
                    "y Luke Skywalker se une a la Alianza Rebelde como piloto de caza.",
                    "Darth Vader persigue implacablemente a los rebeldes.",
                    "Ayuda a Luke a cruzar a través de los meteoritos",
                    "para participar en un ataque contra la Estrella de la muerte",
                    "esta historia es mejor que cualquiera de disney",
                    "pulsa espacio para volver"]
        conta_posiciones = 0

        for mensaje in mensajes:
            texto_render = self.font.render(
                (mensaje), True, (255,255,255))
            self.pantalla.blit(
                texto_render, (pos_x, posiciones[conta_posiciones]))
            conta_posiciones += 1