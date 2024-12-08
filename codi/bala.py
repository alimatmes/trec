import pygame 
from confi import * 
from pygame.math import Vector2 as vector

class Bala(pygame.sprite.Sprite):
    def __init__(self, pos, imatge, direccio, grups):
        super().__init__(grups)
        
        self.image = imatge  # self.image es una propietat de Sprinte, No traduir!
        
        if direccio.x < 0:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = pos)
        self.z = CAPES['principal']

        # float based movement
        self.direccio = direccio
        self.velocitat = 1200
        self.pos = vector(self.rect.center)
        self.temps_inici = pygame.time.get_ticks()

    def update(self,dt):
        self.pos += self.direccio * self.velocitat * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        if pygame.time.get_ticks() - self.temps_inici > 400:
            self.kill()