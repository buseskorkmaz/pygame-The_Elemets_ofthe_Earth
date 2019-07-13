
import pygame
from Source.Arxius import nivells

class Bala(pygame.sprite.Sprite):
    def __init__(self, llista_imatges, pos, estat_pers, previous, color):
        super().__init__()
        self.tipus = color
        self.llista_im = llista_imatges
        self.image = self.llista_im[0]
        self.rect = self.image.get_rect()
        self.rect.left = pos[0]
        self.inicial=pos[0]
        self.rect.top = pos[1]
        self.vel = 3 # Velocitat canvi de sprite 
        self.v = 8 # Velocitat bala
        self.d = estat_pers
        self.p = previous

    def update(self):
        t = pygame.time.get_ticks()
        ta = t % self.vel
        idx = (ta * len(self.llista_im)) // self.vel
        self.image = self.llista_im[idx]
        if self.d == 2:#estat RIGHT
            self.v = 15
        elif self.d == 1:#estat LEFT
            self.v = -15
        else:
            if self.p == 2:
                self.v = 15
            elif self.p == 1:
                self.v = -15
        self.rect.left += self.v
        if abs(self.inicial-self.rect.left)>500:
            self.kill()
