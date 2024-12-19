import pygame,random
from random import choice
from entitat import Entitat
from confi import * 
from pygame.math import Vector2


class Enemic(Entitat):

	def __init__(self, pos, grups, dispara, jugador, collisio_sprites):
		super().__init__(pos, grups, collisio_sprites,dispara)
		
		self.jugador = jugador
		self.direccio = Vector2()
		self.direccio.x=1
		self.posicio = Vector2()
		self.posicio.x = pos[0]
		self.velocitat = 200
		
  		# Per a que caiguin sobre la plataforma
		for sprite in collisio_sprites.sprites():
			if sprite.rect.collidepoint(self.rect.midbottom):
				self.rect.bottom = sprite.rect.top
				self.posicio.y = self.rect.top
		
		
		
		self.temps_refredat = 1000

	def obte_status(self):   # mira a dreta o esquerra segons on estigui el jugador
		# if self.jugador.rect.centerx < self.rect.centerx:
		# 	self.status = 'esquerra'
		# else:
		# 	self.status = 'dreta'
		if self.direccio.x ==1:
			self.status = 'dreta'
		else:
			self.status = 'esquerra'
			
	def import_assets(self):
     
		path = '../personatges/enemics/'
  
		# Esquelet
		self.animacions['dreta'] = [pygame.image.load(f'{path}esquelet/tile00{frame}.png').convert_alpha() for frame in range(8)]
		self.animacions['esquerra'] = [pygame.transform.flip(image,True,False) for image in self.animacions['dreta'] ]


		# Faré un enemic aleatori si tinc temps

	
	def update(self,dt):
		self.obte_status() 
		self.animar(dt)  # a classe mare
  
		self.posicio.x += self.direccio.x * self.velocitat * dt
		self.rect.topleft = (round(self.posicio.x),round(self.posicio.y))  # marca coordenada top esq, round per convertir-ho a enter
  
		self.blink()

  
		# self.temporitzador_dispars()
		self.temporitzador_inmortalitat()
		self.comprova_mort()


class Pinxo(Entitat) :
    def __init__(self, pos, grups, dispara, jugador, collisio_sprites):
        super().__init__(pos, grups, collisio_sprites,dispara)
        
        pass
    def import_assets(self):
        
        path = '../mapa/autum2/'
        self.animacions['esquerra'] = [
            pygame.image.load('../mapa/autum2/pincho.png').convert_alpha(),
            pygame.image.load('../mapa/autum2/pincho.png').convert_alpha()]
		


class Moneda(Entitat):
    def __init__(self, pos, grups, dispara, jugador, collisio_sprites):
        super().__init__(pos, grups, collisio_sprites,dispara)
        
        
        # aLeatori
        
        resultat = random.choice([True, False])
        
        if resultat:  # daurat
            self.status = 'esquerra'
            self.valor=10
        else:  # plata
            self.status = 'dreta'
            self.valor=5
        pass
    def import_assets(self):
        
        path="../mapa/monedes/"
        
		
        self.animacions['esquerra'] = [pygame.image.load(f'{path}gold_coin_0{frame}.png').convert_alpha() for frame in range(1,4)]
        
        
        self.animacions['dreta'] = [pygame.image.load(f'{path}silver_coin_0{frame}.png').convert_alpha() for frame in range(1,4)]
        
    def update(self,dt):     	
      	self.animar(dt)



