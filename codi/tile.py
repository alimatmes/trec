import pygame 
from confi import * 
from pygame.math import Vector2


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, superf, grups,z):#la z es la profunditat a l'hora de pasar per davant i per darrer dels objectes
		super().__init__(grups)
		self.image = superf
		self.rect = self.image.get_rect(topleft = pos)
		self.z =z # Per ficar profunditat , < més al fons

class CollisionTile(Tile):
	def __init__(self, pos, superf, grups):
		super().__init__(pos,superf,grups, CAPES['principal'])
		self.old_rect = self.rect.copy()#primer mira on estaba abans per a les col·lisions (repasar per a entedre-ho millor)66g


class PujaBaixa(CollisionTile):
	def __init__(self,pos,superf,grups):
		super().__init__(pos,superf,grups)

		# float based movement
		#self.tipus='pujabaixa'   # per a evitar que el jugador xoqui amb l'ascensor
		self.direccio = Vector2(0,-1)
		self.velocitat = 100
		# self.rect.width=64
		# self.rect.wdth=32
		self.posicio = Vector2(self.rect.topleft)

	def update(self,dt):  # Com que es mou, s'ha d'actualitzar
		self.old_rect = self.rect.copy()  # per mirar quan xoqui
		self.posicio.y += self.direccio.y * self.velocitat * dt
		self.rect.topleft = (round(self.posicio.x),round(self.posicio.y))  # marca coordenada top esq, round per convertir-ho a enter