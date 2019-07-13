
import pygame

class Selector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # constructor de classe Sprite
        self.image = pygame.image.load("Source/Imatges/sword.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image = pygame.transform.rotate(self.image,-45)
        self.rect = self.image.get_rect()  # rectangle de la imatge
        self.menus = [580,560], [930,680], [200,680]
        self.sel = 0
        self.rect.center = self.menus[self.sel]


    def up(self):
        if self.sel == 0:
            self.sel = 2
        else:
            self.sel -= 1
        self.rect.center = self.menus[self.sel]


    def down(self):
        if self.sel == len(self.menus)-1:
            self.sel = 0
        else:
            self.sel += 1
        self.rect.center = self.menus[self.sel]

    def select(self):
        return self.sel
