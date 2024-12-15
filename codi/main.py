import pygame, sys 
from bala import Bala
from confi import *
from pytmx.util_pygame import load_pygame

from player import Jugador
from enemic import Enemic, Pinxo, Moneda
from tile import Tile,CollisionTile, PujaBaixa
from finaljoc import Final

from pygame.math import Vector2 as vector 
from sobreposat import Sobreposat

# Aquesta classe és un grup, que hereda de grup
# La utilitzem per poder pintar els sprites amb offset
class TotsSprites(pygame.sprite.Group):

	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()
  
		self.cel_davant = pygame.image.load('../personatges/background/fg_sky.png').convert_alpha()
		self.cel_fons = pygame.image.load('../personatges/background/bg_sky.png').convert_alpha()
  
		tmx_map = load_pygame('../mapa/n_1.tmx') # els dos punts es per a tirar enrere de la carpeta
  
		self.padding = BASE/2
		self.ample_cel = self.cel_fons.get_width()
		mapa_ample = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
		self.num_cels = int(mapa_ample // self.ample_cel) + 1
		

	def dibuixa_sprites(self,jugador,mapx, mapy):  # Per calcular amb l'offset, ho pinta tot, sprites patrons

		# Canvia l'offset
		
		self.offset.y = jugador.rect.centery - ALTURA / 2
		# Control·lem l'offset a la X
		# quan arribi a la banda esquerra, a la meitat, deixa de fer-se scroll
		if jugador.rect.centerx < BASE/2:
			self.offset.x=0
		elif jugador.rect.centerx > mapx - BASE/2:
			# print(self.offset.x)
			# print(jugador.rect.x)
			self.offset.x =   mapx - BASE   # la pantalla para  , offset a esquerra
		else:
			self.offset.x = jugador.rect.centerx - BASE / 2

		if jugador.rect.centery < ALTURA/2:
			self.offset.y=-32
		elif jugador.rect.centery > mapy - ALTURA/2:
			self.offset.y = mapy -ALTURA -32

		else:
			self.offset.y = jugador.rect.centery - ALTURA/2 -32
		
		for x in range(self.num_cels):
			# exercise: place all of the skies in the display surface 
			x_pos = -self.padding + (x * self.ample_cel)
			self.display_surface.blit(self.cel_fons,(x_pos - self.offset.x / 2.5, 100 - self.offset.y / 2.5))
			self.display_surface.blit(self.cel_davant,(x_pos - self.offset.x / 2, 100 - self.offset.y / 2))


		# print (self.offset)
		# print (jugador.rect.centerx)
		
		

		# Pinta tots els sprites
		# for sprite in self.sprites(): # sorted(self.sprites(), key = lambda sprite: sprite.z):
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):

			offset_rect = sprite.image.get_rect(center = sprite.rect.center)
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image, offset_rect)



class Principal:

	def __init__(self): #constructor quan creo l'objecte
		
		pygame.init()
  
  
		self.display_surface = pygame.display.set_mode((BASE, ALTURA))
		pygame.display.set_caption('TDR Alícia Mata')
		self.rellotge = pygame.time.Clock()

		# grups --> ara la classe TotsSprites
		self.tots_sprites = TotsSprites()  # tots els sprites
		self.collisio_sprites = pygame.sprite.Group()  # grup per a lo que col·lisiona 
		self.pujabaixa_sprites = pygame.sprite.Group()  # grup per als pujabaixa
		self.bala_sprites = pygame.sprite.Group()   # Grup per a les bales que es disparen
		self.enemic_sprites = pygame.sprite.Group()
		self.vulnerable_sprites = pygame.sprite.Group()  # els que es poden fer mal i perdre salut
		self.moneda_sprites = pygame.sprite.Group()
		self.bala_imatge = pygame.image.load('../personatges/foc_enemic/tile000.png').convert_alpha()
		self.bala_imatge = pygame.transform.scale_by(self.bala_imatge,0.5)
		self.bala_imatge = pygame.transform.flip(self.bala_imatge,True,False)
  
		self.color = (255, 255, 0)
		self.tmx_map = None

		self.setup()#per a dibuixar el mapa (linea: 75)
		self.sobreposat = Sobreposat(self.jugador)
  
		self.musica = pygame.mixer.Sound('../musica/Village4.mp3')
		self.musica.play(loops = -1)

		# sprites 
		# self.jugador = Jugador((100,40),self.tots_sprites, self.collisio_sprites)
		# self.enemic = Enemic((100,200),self.tots_sprites)


	def setup(self):
		
		tmx_map = load_pygame('../mapa/n_1.tmx') # els dos punts es per a tirar enrere de la carpeta
		
		self.tmx_map = tmx_map
		patro_ample = tmx_map.tilewidth  # Ancho de cada tile en píxeles
		map_ample = tmx_map.width
		map_altura = tmx_map.height
		patro_altura = tmx_map.tilewidth

		# Mida del mapa en pixels
		self.mapx= patro_ample*map_ample
		self.mapy= patro_altura*map_altura

		for x,y, superf in tmx_map.get_layer_by_name('darrere').tiles():#recorra tots els patrons de la capa darrere
			Tile((x * 32,y * 32 - superf.get_rect().height), superf, self.tots_sprites,CAPES['darrere'])


		for x,y, superf in tmx_map.get_layer_by_name('principal').tiles():#el mateix però en aquesta capa i a més estan els patrons amb els que col·lisiones
			CollisionTile((x * 32,y * 32 - superf.get_rect().height), superf, [self.tots_sprites,self.collisio_sprites])

		for x,y, superf in tmx_map.get_layer_by_name('davant').tiles():
			Tile((x * 32,y * 32 - superf.get_rect().height), superf, self.tots_sprites,CAPES['davant'])

		
		self.tope_rect_enemic_mobil = []
		self.tope_final_joc = []   # Punts on pot acabar el joc
		for obj in tmx_map.get_layer_by_name('entitats'):
			if obj.name == 'moneda':
				Moneda(
					pos=(obj.x,obj.y-32),
           			grups= [self.tots_sprites,self.moneda_sprites],
              		dispara= self.dispara, 
                	jugador= self.jugador,
                 	collisio_sprites= self.collisio_sprites)
      
			if obj.name == 'pinxo':
				Pinxo(
					pos=(obj.x,obj.y-32),
           			grups= [self.tots_sprites,self.enemic_sprites],
              		dispara= self.dispara, 
                	jugador= self.jugador,
                 	collisio_sprites= self.collisio_sprites)
				
			if obj.name == 'jugador':
				self.jugador = Jugador(  # presentat aqixí queda més clar
        			pos= (obj.x,obj.y), 
           			grups = [self.tots_sprites,self.vulnerable_sprites],
              		collisio_sprites = self.collisio_sprites,
                	dispara= self.dispara)
			if obj.name == 'enemic_mobil':   # No se si dispararà
				Enemic(
        			pos=(obj.x,obj.y),
           			grups= [self.tots_sprites,self.enemic_sprites,self.vulnerable_sprites],
              		dispara= self.dispara, 
                	jugador= self.jugador,
                 	collisio_sprites= self.collisio_sprites)
			if obj.name =='tope':
				tope_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
				self.tope_rect_enemic_mobil.append(tope_rect)  

			if obj.name == 'finaljoc':
				final_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
				self.tope_final_joc.append(final_rect)  # afegeix a la llista


		self.tope_rect_pujabaixa = []
		for obj in tmx_map.get_layer_by_name('ascensors'):
			if obj.name == 'pujabaixa':
				PujaBaixa((obj.x,obj.y),obj.image,[self.tots_sprites, self.collisio_sprites, self.pujabaixa_sprites])
			else: #  si no es la plataforma de l'ascensor, dibuixa rectangle i l'afegeix a la llista
				tope_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
				self.tope_rect_pujabaixa.append(tope_rect)  # afegeix a la llista
	def collisio_final(self):
     
		for vora in self.tope_final_joc:  # Comprovem si xoca amb el rectangle de la capa "ascensors"
				if self.jugador.rect.colliderect(vora): #
					print("El joc ha acabat")
					return True
		return False


	def collisio_bala(self):
     	# obstacles 
		for obstacle in self.collisio_sprites.sprites():
			pygame.sprite.spritecollide(obstacle,self.bala_sprites,True)
			# Sl el tercer par+àmetre és True, mata l'sprite xocant, quan hi ha col·lisió
    
		# entitats
		for sprite in self.vulnerable_sprites.sprites():
			if pygame.sprite.spritecollide(sprite, self.bala_sprites, True):
				print("holaaa")
				sprite.dany()

	def collisio_monedes(self):
		for mon in self.moneda_sprites.sprites():
			if mon.rect.colliderect(self.jugador): # quan arriba als topes
				self.jugador.puntuar(mon.valor)
				mon.kill()
    
	def collisio_enemic_mobil(self):
		
		for enem in self.enemic_sprites.sprites():
			# Col·lisó amb rectangles, per fer canvi de sentit
			for vora in self.tope_rect_enemic_mobil:  # Comprovem si xoca amb el rectangle de la capa "ascensors"
				if enem.rect.colliderect(vora): # quan arriba als topes
					if enem.direccio.x < 0: #up
						enem.rect.left = vora.right
						enem.posicio.x = enem.rect.x
						enem.direccio.x = 1
						
					else: # down
						enem.rect.right = vora.left
						enem.posicio.x = enem.rect.x
						enem.direccio.x = -1
			# Col·lisió amb el juegaodr
			if enem.rect.colliderect(self.jugador):
				self.jugador.dany()
   
	def collisio_pujabaixa(self): # detectem quan algu colisiona, el jugador basicament
		for plat in self.pujabaixa_sprites.sprites():
			for vora in self.tope_rect_pujabaixa:  # Comprovem si xoca amb el rectangle de la capa "ascensors"
				if plat.rect.colliderect(vora): # quan arriba als topes
					if plat.direccio.y < 0: #up
						plat.rect.top = vora.bottom
						plat.posicio.y = plat.rect.y
						plat.direccio.y = 1
						
					else: # down
						plat.rect.bottom = vora.top
						plat.posicio.y = plat.rect.y
						plat.direccio.y = -1
			
			if plat.rect.bottom == self.jugador.rect.top or plat.rect.bottom == self.jugador.rect.top + 1 : #and self.jugador.a_terra == True:
				
				if self.jugador.rect.left >= plat.rect.left and self.jugador.rect.left <= plat.rect.right:
					plat.rect.bottom = self.jugador.rect.top
					plat.posicio.y = plat.rect.y
					plat.direccio.y = -1
					print(self.jugador.rect.left)
					print(plat.rect.left)
				elif self.jugador.rect.right >= plat.rect.left and self.jugador.rect.right <= plat.rect.right:
					plat.rect.bottom = self.jugador.rect.top
					plat.posicio.y = plat.rect.y
					# self.jugador.rect.top = plat.rect.bottom
					plat.direccio.y = -1
				elif self.jugador.rect.centerx >= plat.rect.left and self.jugador.rect.centerx <= plat.rect.right:
					plat.rect.bottom = self.jugador.rect.top
					plat.posicio.y = plat.rect.y
					# self.jugador.rect.top = plat.rect.bottom
					plat.direccio.y = -1
			# Si el jugador no
			#  esta a terra i la plataforma baixa, l'arrastra
			# Com arreglar-ho?
	
			# no funciona 
			# if plat.rect.colliderect(self.jugador.rect):
			# 	print ("ha xoat jugador i plataforma")
			# 	if self.jugador.rect.centery > plat.rect.centery:
			# 		plat.rect.bottom = self.jugador.rect.top
			# 		plat.posicio.y = plat.rect.y
			# 		plat.direccio.y = -1
	def dispara(self, pos, direccio, entitat):
		Bala(pos, self.bala_imatge, direccio, [self.tots_sprites, self.bala_sprites])
	
	def run(self):
		while True:
			# event loop 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			# delta time 
			dt = self.rellotge.tick() / 1000
			self.display_surface.fill((135, 206, 235))

			self.collisio_pujabaixa()
			self.tots_sprites.update(dt)
   
			self.collisio_bala()
			self.collisio_enemic_mobil()
			self.collisio_monedes()
			if self.collisio_final():
				final= Final()
				final.run()
			self.tots_sprites.dibuixa_sprites(self.jugador, self.mapx, self.mapy)

			self.sobreposat.mostra()
		
  
  
				
			# actualitza display 
			pygame.display.update()


 
 	# principal = Principal()
	# principal.run()
 