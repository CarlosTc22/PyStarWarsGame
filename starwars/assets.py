import os
import pygame as pg
from . import ALTO, ANCHO, MARGEN_NAVE , VELOCIDAD

class X_Wing ():
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
