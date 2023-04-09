import os
import random
import pygame as pg
from . import ALTO, ANCHO, MARGEN_NAVE , VELOCIDAD

class X_Wing ():

    # Se crea la nave y se le da movimiento arriba y abajo pulsando esas teclas

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("resources", "images", "X_Wing.png"))
        self.rect = self.image.get_rect(midbottom=(MARGEN_NAVE, ALTO/2))
   

    def update(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_UP]:
            self.rect.y -= VELOCIDAD
            if self.rect.top < 0:
                self.rect.top = 0

        if teclas[pg.K_DOWN]:
            self.rect.y += VELOCIDAD
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

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