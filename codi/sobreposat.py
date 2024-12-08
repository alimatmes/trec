import pygame

class Sobreposat:
    def __init__(self,jugador):
        self.jugador = jugador
        self.display_surface = pygame.display.get_surface()
        self.imatge_salut = pygame.image.load('../personatges/salut/salut.png').convert_alpha()

    def mostra(self):
        for h in range(self.jugador.salut):
            x = 30 + h * (self.imatge_salut.get_width() + 4)
            y = 20
            self.display_surface.blit(self.imatge_salut,(x,y))
                
        for h in range(self.jugador.vides):
            x = 170 + h * (self.imatge_salut.get_width() + 4)
            y = 20
            self.display_surface.blit(self.imatge_salut,(x,y))