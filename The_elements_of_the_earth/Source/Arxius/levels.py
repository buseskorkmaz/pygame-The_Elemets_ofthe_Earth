import pygame
 
class Platform(pygame.sprite.Sprite):
 
    def __init__(self, posicio,  nom_fitxer_imatge):
        super().__init__() # constructor de classe Sprite
        self.image = pygame.image.load(nom_fitxer_imatge).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # rectangle de la imatge
        self.rect.left = posicio[0]
        self.rect.top = posicio[1]
 
