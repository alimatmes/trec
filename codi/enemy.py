import pygame 
from os import walk
from random import choice

from settings import * 


class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,grups):
		super().__init__(grups)
		
		for _, _, img_list in walk('../graphics/enemies'):
			print(img_list)
			enemy_name = choice(img_list)

		self.image = pygame.image.load('../graphics/enemies/' + enemy_name).convert_alpha()
		# el fem més petit, que la imatge és molt gran
		self.image = pygame.transform.scale(self.image,(32,32))
		self.rect = self.image.get_rect(center = pos)

		# float based movement 
		self.pos = pygame.math.Vector2(self.rect.center)
		print (self.pos)

		self.z = CAPES['principal']

		
		if pos[0] < 200:
			self.direccio = pygame.math.Vector2(1,0)
		else:
			self.direccio = pygame.math.Vector2(-1,0)
			self.image = pygame.transform.flip(self.image,True, False)

		self.speed = 100

	def update(self,dt):
		self.pos += self.direccio * self.speed * dt
		self.rect.center = (round(self.pos.x), round(self.pos.y))

		if not -200 < self.rect.x < 3400:
			self.kill()