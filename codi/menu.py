import pygame,sys
from confi import *
from main import Principal

class Menu:
    def __init__(self):
        
        pygame.init()

        #---Crear ventana
        ventana= pygame.display.set_mode((BASE,ALTURA))

        #Fons
        fons_introduccio=pygame.image.load('../fotos/PantallaMenu.png')
        ventana.blit(fons_introduccio, (0,0))

        fuente_introduccio_1=pygame.font.Font("../text/hola.ttf", 100)
        fuente_introduccio_2=pygame.font.Font("../text/hola.ttf", 50)
        fuente_introduccio_3=pygame.font.Font("../text/hola.ttf", 25)


        #---Text
        introduccio_1= fuente_introduccio_1.render('Benvingut', 1, '#664e1b') 
        ventana.blit (introduccio_1, (550,220))

        introduccio_2=fuente_introduccio_2.render('Per a començar apreta SPACE', 1, 'Black')
        ventana.blit (introduccio_2, (425, 350))
        
        introduccio_3=fuente_introduccio_3.render('TREC Alícia Mata (2024)', 1, 'Black')
        ventana.blit (introduccio_3, (600, 450))
        
        # self.musica = pygame.mixer.Sound('../musica/000001.mp3')
        # self.musica.play(loops = -1)   
       
    def run (self):
        while True:
			# event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
				# horizontal input 
                if keys[pygame.K_SPACE]:    
                    print ("A JUGAR!!!!!!")
                    principal = Principal()
                    principal.run()
                    

                

            pygame.display.update()

if __name__ == '__main__': #això és per asegurar que això nomes s'executa en aquest arxiu
	
	menu = Menu()
	menu.run()