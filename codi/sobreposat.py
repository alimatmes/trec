import pygame

class Sobreposat:
    def __init__(self,jugador):
        self.jugador = jugador
        self.imatge_display = pygame.display.get_surface()
        self.imatge_salut = pygame.image.load('../personatges/salut/salut.png').convert_alpha()
        self.imatge_vides = pygame.image.load('../personatges/salut/vides.png').convert_alpha()


        self.font_salut=pygame.font.Font("../text/hola.ttf", 35)
        self.font_punts=pygame.font.Font("../text/Arcade.ttf", 55)

    def mostra(self):
        salut = self.font_salut.render('Salut', 1, '#664e1b') 
        self.imatge_display.blit (salut, (40,30))
        
        for h in range(self.jugador.salut):
            x = 150 + h * (self.imatge_salut.get_width() + 4)
            y = 40
            self.imatge_display.blit(self.imatge_salut,(x,y))

        vides = self.font_salut.render('Vides', 1, '#664eff') 
        self.imatge_display.blit (vides, (275,30))
        for h in range(self.jugador.vides):
            x = 390 + h * (self.imatge_vides.get_width() + 4)
            y = 40
            self.imatge_display.blit(self.imatge_vides,(x,y))

        punts = self.font_salut.render('Punts: ' , 1, '#664e1b') 
        self.imatge_display.blit (punts, (470,30))
        point = str(self.jugador.puntuacio)
        punts = self.font_punts.render(point , 1, 'White') 
        self.imatge_display.blit (punts, (590,34))
