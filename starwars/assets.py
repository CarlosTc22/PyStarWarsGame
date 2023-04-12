import os
import random
import pygame as pg
from . import ALTO, ANCHO, MARGEN_NAVE , VELOCIDAD

class X_Wing():
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("resources", "images", "X_Wing.png"))
        self.rect = self.image.get_rect(midbottom=(MARGEN_NAVE, ALTO/2))
        self.colision_time = 0  # Tiempo de espera después de la colisión
        self.hay_colision = False  # Indicador de colisión

    def update(self):
        if self.rect.y >= 0: # No funciona el movimiento si no está en pantalla
            teclas = pg.key.get_pressed()
            if teclas[pg.K_UP]:
                self.rect.y -= VELOCIDAD
                if self.rect.top < 0:
                    self.rect.top = 0

            if teclas[pg.K_DOWN]:
                self.rect.y += VELOCIDAD
                if self.rect.bottom > ALTO:
                    self.rect.bottom = ALTO

    def detectar_colision(self, nivel_facil):
        # Verificar si la nave está colisionando con un meteorito
        for meteorito in nivel_facil.meteoritos:
            if self.rect.colliderect(meteorito.rect):
                self.hay_colision = True
                self.colision_time = pg.time.get_ticks()  # Obtener el tiempo actual en milisegundos
                nivel_facil.meteoritos.remove(meteorito)
                break

class Ball_Training():

    # Creo la bola de entrenamiento Jedi que sube y baja por decoración, no tiene otra función

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("resources", "images", "ball_training.png"))
        self.image = pg.transform.scale(self.image, (self.image.get_width()//2, self.image.get_height()//2))
        self.rect = self.image.get_rect(midbottom=(ANCHO - MARGEN_NAVE, ALTO/2))
        self.direction = 1  

    def update(self):
        if self.rect.bottom >= ALTO or self.rect.top <= 0:
            self.direction *= -1  
        self.rect.y += self.direction * 1  

class Laser():

    # Se generan disparos laser aleatorios de entrenamiento, estos NO hacen daño

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("resources", "images", "laser.png"))
        y = random.randint(0, ALTO - self.image.get_height())
        self.rect = self.image.get_rect(midbottom=(ANCHO - MARGEN_NAVE, y))
        self.velocidad = 2

    def update(self):
        self.rect.x -= self.velocidad

class Meteorito():
    def __init__(self):
        super().__init__()
        self.width = random.randint(20, 120)
        self.height = random.randint(20, 120)
        IMAGENES_METEORITO = [
        "asteroid1.png",
        "asteroid2.png",
        "asteroid3.png",
        "asteroid4.png"
        ]
        # Seleccionar una imagen aleatoria de la lista
        imagen_aleatoria = random.choice(IMAGENES_METEORITO)
        self.image = pg.image.load(os.path.join("resources", "images", imagen_aleatoria)).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(midbottom=(ANCHO - MARGEN_NAVE, random.randint(0, ALTO - self.height)))
        self.velocidad = random.randint(1, 4)
        self.cruzado_eje_x = False
        
    def update(self):
        self.rect.x -= self.velocidad

