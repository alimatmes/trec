import pygame,sys
from confi import *

class Final:
    def __init__(self, puntuacio):
        
        pygame.init()

        #---Crear ventana
       
        ventana= pygame.display.set_mode((BASE,ALTURA))

        self.musica = pygame.mixer.Sound('../musica/musicafinal.wav')
        self.musica.set_volume(0.6)  # Volumen bajo al 30%
        self.musica.play(loops = -1)


        #Fons
        fons_introduccio=pygame.image.load('../fotos/fondo_final.png')
        ventana.blit(fons_introduccio, (0,0))

        fuente_introduccio_1=pygame.font.Font("../text/hola.ttf", 80)
        
        fuente_introduccio_3=pygame.font.Font("../text/hola.ttf", 40)

        font_punts=pygame.font.Font("../text/Arcade.ttf", 85)
        font_space=pygame.font.Font("../text/Arcade.ttf", 45)



        introduccio_3=fuente_introduccio_3.render('TREC Alícia Mata (2024)', 1, 'Black')
        ventana.blit (introduccio_3, (400, 50))

        #---Text
        introduccio_1= fuente_introduccio_1.render('Puntuació', 1, '#664e1b') 
        ventana.blit (introduccio_1, (425,200))

        introduccio_2=font_punts.render(str(puntuacio) + ' punts', 1, 'Black')
        ventana.blit (introduccio_2, (500, 310))
        
  

        prem_tecla=font_space.render(' Prem la tecla space per continuar', 1, 'Black')
        ventana.blit (prem_tecla, (275, 400))
        
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
                    from menu import Menu

                    self.musica.stop()   
                    menu = Menu()
                    menu.run()
                    

                

            pygame.display.update()