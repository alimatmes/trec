import pygame
from confi import * 
from pygame.math import Vector2
from math import sin


class Entitat(pygame.sprite.Sprite):
    def __init__(self, pos, grups,collisio_sprites,dispara):
        super().__init__(grups)
		# dispara és un mètode de la classe Principal
		# image 

        self.animacions={}
        self.import_assets()
        
        self.frame_index = 0
        
        
        self.image = self.animacions['esquerra'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.status = 'dreta'
        
        self.jugador = None

        self.z = CAPES['principal']




		# float based movement 
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direccio = pygame.math.Vector2()
        self.speed = 200

		# col·lisio
        

        
		# Per al foc
        self.pot_disparar = True	# si pot disparar
        self.temps_dispar = None     # temps que dispara
        self.temps_refredat = 200    # temps entre dispars
        self.dispara = dispara
        
        # Salut
        self.salut_inicial = 5
        self.salut = self.salut_inicial
        
        self.es_vulnerable = True
        self.temps_collisio = None
        self.durada_inmortalitat = 800

        self.impacta_bala = pygame.mixer.Sound('../musica/impacte_bala.wav')
        self.more_enemic = pygame.mixer.Sound('../musica/more_enemic.wav')


    
    # temps que si hi ha collisio , no compta
    # quan enemic xoca, es fan multiples col·lisions, i es more ràpid
    def temporitzador_inmortalitat(self):
        if not self.es_vulnerable:
            temps_actual = pygame.time.get_ticks()
            if temps_actual - self.temps_collisio > self.durada_inmortalitat:
                self.es_vulnerable = True

    def temporitzador_dispars(self):
        if not self.pot_disparar:
            temps_actual = pygame.time.get_ticks()
            if temps_actual - self.temps_dispar > self.temps_refredat:
                self.pot_disparar = True
    
    
    ## L'animació del personatge, quan camina, etc
    def animar(self,dt):

        status=self.status
        current_animation = self.animacions[status]
        self.frame_index += 10 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
    
    def import_assets(self):
        pass
    
    def blink(self):  
        if not self.es_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                superficie_blanca = mask.to_surface()
                superficie_blanca.set_colorkey((0,0,0))
                self.image = superficie_blanca

    def wave_value(self):  
        value = sin(pygame.time.get_ticks())
        
        if value >= 0: 
            return True
        else:
            return False
        
    def dany(self):
        if self.es_vulnerable:   
            # self.salut -= 1
            self.salut -= 1
            self.es_vulnerable = False
            self.temps_collisio = pygame.time.get_ticks()  # temps actual
            self.impacta_bala.play()



    def puntuar(self,valor):
        
        
        self.puntuacio += valor
        
    def comprova_mort(self):

        if self.salut <=0:
            self.jugador.puntuar(20)
            self.more_enemic.play()


            self.kill()
        
        
