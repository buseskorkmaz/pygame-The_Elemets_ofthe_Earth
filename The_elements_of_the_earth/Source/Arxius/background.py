import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, imatge, valor, pos):
        super().__init__() # constructor de classe Sprite
        self.image = pygame.image.load(imatge).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10000, 720))
        self.rect = self.image.get_rect()  # rectangle de la imatge
        self.pos=pos
        self.val=valor
    def world_shift(self, shift_x):
        self.rect.left = self.pos+ shift_x//self.val
        



