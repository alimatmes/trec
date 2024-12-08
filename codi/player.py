import pygame, sys
from confi import * 
from pygame.math import Vector2
from entitat import Entitat
## Mètodes i propietats per al jugador
##  Col·lisions, animacions, moviment, etc

class Jugador(Entitat):
	def __init__(self, pos, grups,collisio_sprites,dispara):
		super().__init__(pos, grups,collisio_sprites,dispara)
		# dispara és un mètode de la classe Principal
		# image 
	
		self.posicio_inicial = pos
	
		self.collisio_sprites = collisio_sprites

		self.gravetat = 15
		self.velocitat_salt = 1000
		self.a_terra  = False
		self.movent_terra = None   # Per a evitar l'efecte extranys quan el jugador baixa a l'ascensor
		self.ajupit = False
	
		self.vides = 3

		

	
    ## Carrega tots els sprites del jugador  <-- 
	def import_assets(self):  # us de diccionari !
		#super().import_assets()
  
		#self.animacions = {}
		path = '../personatges/'
		# Carrego les imatges a la dreta
		self.animacions['dreta'] = [pygame.image.load(f'{path}personatge_2/tile00{frame}.png').convert_alpha() for frame in range(4)]
		# inverteixo a l'esquerra
		self.animacions['esquerra'] = [pygame.transform.flip(image,True,False) for image in self.animacions['dreta'] ]
		# No són animacions, però ho podrien ser, fem igualment un array per aprofitar codi
		self.animacions['quiet_dreta'] = [pygame.image.load(f'{path}personatge_quiet/tile005_quiet.png').convert_alpha()]
		self.animacions['quiet_esquerra'] = [pygame.transform.flip(image,True,False) for image in self.animacions['quiet_dreta'] ]
		self.animacions['salt_dreta'] = [pygame.image.load(f'{path}personatge_salt/salt_dreta.png').convert_alpha()]
		self.animacions['salt_esquerra'] = [pygame.transform.flip(image,True,False) for image in self.animacions['salt_dreta'] ]
		self.animacions['caient_dreta'] = [pygame.image.load(f'{path}personatge_salt/caient_dreta.png').convert_alpha()]
		self.animacions['caient_esquerra'] = [pygame.transform.flip(image,True,False) for image in self.animacions['caient_dreta'] ]
		# foc animacions   -> de moment no ho faig. No es nota massa
		# self.animacions['foc_esquerra'] = [pygame.image.load(f'{path}foc_enemic/tile00{frame}.png').convert_alpha() for frame in range(6)]
		# self.animacions['foc_esquerra'] = [pygame.transform.scale_by(image,0.4) for image in self.animacions['foc_esquerra'] ]  # escalo
		# self.animacions['foc_dreta'] = [pygame.transform.flip(image,True,False) for image in self.animacions['foc_esquerra'] ]

	def obte_status(self):  # comprovo com estic per posar un sprite o un altre
							# Una part es fa a l'input		
		
		# salta
		if self.direccio.y < 0 and self.a_terra == False:  #saltant
			if self.direccio.x > 0: # es mou a la dreta
				self.status = 'salt_dreta'
			elif self.direccio.x < 0: # es mou a l'esquerra
				self.status = 'salt_esquerra'
			else:
				if self.status=="quiet_dreta":
					self.status = 'salt_dreta'
				if self.status=="quiet_esquerra":
					self.status = 'salt_esquerra'
		elif self.direccio.y > 0 and self.a_terra == False:   # està caient
			if self.direccio.x > 0: # es mou a la dreta
				self.status = 'caient_dreta'
			elif self.direccio.x < 0: # es mou a l'esquerra
				self.status = 'caient_esquerra'
		elif self.direccio.y == 0 and self.a_terra == True:  # toca terra
			if self.direccio.x > 0: # es mou a la dreta
				self.status = 'dreta'
			elif self.direccio.x < 0: # es mou a l'esquerra
				self.status = 'esquerra'
			else:
				# Quan cau es queda en posicio de salt o de caure, per a que es posi en quiet dreta o esquerra
				if self.status == 'dreta' or self.status == 'caient_dreta' or self.status == 'salt_dreta':
					self.status = 'quiet_dreta'
				if self.status == 'esquerra' or self.status == 'caient_esquerra' or self.status == 'salt_esquerra':
					self.status = 'quiet_esquerra'
				
		


	def collision(self, direccio):
		for sprite in self.collisio_sprites.sprites():
			if sprite.rect.colliderect(self.rect):

				if direccio == 'horizontal':
					# esquerra collision
					if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
						self.rect.left = sprite.rect.right
					# dreta collision
					if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
						self.rect.right = sprite.rect.left
					self.pos.x = self.rect.x
				else:
					if self.rect.bottom + 10  >= sprite.rect.top  and self.old_rect.bottom <= sprite.old_rect.top:
						self.rect.bottom = sprite.rect.top
						self.a_terra = True    

					if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
						self.rect.top = sprite.rect.bottom
					self.pos.y = self.rect.y
					self.direccio.y = 0 # que no es mogui en vertical, si no fa coses rares
		
		if self.a_terra and self.direccio.y != 0:   # si s'esta movent amunt o avall i toca a terra
			self.a_terra = False   # no ha de tocar
		

	def comprova_contacte(self):   # saber si està a terra o ja saltava, per a no tenir molts salts a l'hora
		bottom_rect = pygame.Rect(0,0,self.rect.width,5)  # crea un rectangle de 5 pixels d'alt, mateixa amplada que el jugador
		bottom_rect.midtop = self.rect.midbottom # El fica just a sota del jugador
		for sprite in self.collisio_sprites.sprites():   # comprova si xoca aquest minirectangle
			if sprite.rect.colliderect(bottom_rect):      # si xoca és que està a terra o quasi a terra (5 pixels amunt)  
				if self.direccio.y > 0:   # si està caient 
					self.a_terra = True
				if hasattr(sprite,'direccio'):
					self.movent_terra = sprite


	def move(self,dt):

		# normalize a vector -> the length of a vector is going to be 1
		# if self.direccio.magnitude() != 0:
		# 	self.direccio = self.direccio.normalize()

		self.pos.x += self.direccio.x * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')

		# moviment vertical
		self.direccio.y += self.gravetat
		self.pos.y += self.direccio.y * dt

		# Enganxa el jugador a la plataforma-ascensor
		# if self.movent_terra  and self.movent_terra.direccio.y > 0 and self.direccio.y > 0:
		# 	self.direccio.y = 0
		# 	self.rect.bottom = self.movent_terra.rect.top
		# 	self.pos.y = self.rect.y
		# 	self.a_terra = True

		# if self.movent_terra  and self.movent_terra.direccio.y < 0 and self.direccio.y < 0:
			
		# 	self.direccio.y = 0
		# # 	self.rect.bottom = self.movent_terra.rect.top
		# 	self.pos.y = self.rect.y
		# 	self.a_terra = True

		self.rect.y = round(self.pos.y)
		self.collision('vertical')

		self.movent_terra = None  # Si no el posem així es queda per sempre i tornen a passar coses rarres


		# self.pos += self.direccio * self.speed * dt
		# self.rect.center = (round(self.pos.x), round(self.pos.y))

	def input(self):#funcio per a moure el personatge amb les tecles
		keys = pygame.key.get_pressed()
		
		# horizontal input 
		if keys[pygame.K_RIGHT]:
			self.direccio.x = 1.28
			self.status='dreta'



		elif keys[pygame.K_LEFT]:
			self.direccio.x = -1.28
			self.status='esquerra'
		else:
			self.direccio.x = 0
			if self.status == 'dreta':
				self.status = 'quiet_dreta'
			elif self.status == 'esquerra':
				self.status = 'quiet_esquerra'
				

		if keys[pygame.K_UP] and self.a_terra:  # Salta si està a terra , fa rebot (mirar)
			self.direccio.y = -self.velocitat_salt
			if self.status == 'dreta':   # no funciona aqui 
				self.status = 'salt_dreta'
			elif self.status == 'esquerra':
				self.status = 'salt_esquerra'

		if keys[pygame.K_DOWN]:   # de moment no ho faig servir
			self.ajupit = True
		else:
			self.ajupit = False
		
		if keys[pygame.K_SPACE] and self.pot_disparar:
			if 'dret' in self.status:   # corre, salta, quiet
				direccio = Vector2(1,0) 
				y_offset = Vector2(-17,-30)
			else:
				direccio = Vector2(-1,0)
				y_offset = Vector2(37,-30)
    
			pos = self.rect.center + direccio * 60
			self.dispara(pos + y_offset, direccio, self)

			self.pot_disparar = False
			self.temps_dispar = pygame.time.get_ticks()
    ## L'animació del personatge, quan camina, etc
	def animar(self,dt):

		status=self.status
		current_animation = self.animacions[status]
		self.frame_index += 10 * dt
		if self.frame_index >= len(current_animation):
			self.frame_index = 0
		self.image = current_animation[int(self.frame_index)]

	def comprova_mort(self):  # resscrivim la d'entitat
							  # perque si és el jugador qui more acaba diferent
		if self.salut <= 0:
			if self.vides > 0:
				print("oeoeoeoe")
				self.vides -= 1
				self.salut=self.salut_inicial

				print(self.salut)		
				print (self.rect.topleft)
				self.rect = self.image.get_rect(topleft = self.posicio_inicial)
				self.pos.x = self.rect.x
				self.pos.y = self.rect.y
			else:
				pygame.quit()
				sys.exit()
       
	def update(self,dt):

		self.old_rect = self.rect.copy()
		self.input()
		self.obte_status()
		self.move(dt)
		self.comprova_contacte()
		self.animar(dt)
		self.blink()

  
		self.temporitzador_dispars()
		self.temporitzador_inmortalitat()
  
		self.comprova_mort()