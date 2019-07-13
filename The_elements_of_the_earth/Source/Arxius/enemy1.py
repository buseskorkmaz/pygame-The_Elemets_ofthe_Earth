import pygame
from Source.Arxius import conf
class Animacio(pygame.sprite.Sprite):

    # Inicialitza els estats. Són nombres enters.
    NO_ATTACK, ATTACK, DIE =  1, 1, 0
    # Inicialitza les transicions
    WAIT, GO_ATTACK,  GO_DIE = range(3)

    def __init__(self, mat_l, mat_r, pos, color):
        super().__init__()
        # Defineix l'estat inicial
        self.estat = self.NO_ATTACK
        self.d = "left"
        self.tipus = color
        self.mat_l = mat_l
        self.mat_r = mat_r
        self.llista_im = self.mat_l
        self.count = 0
        self.nframes = len(self.llista_im[0])
        self.image = self.llista_im[self.estat][0]
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.top=pos[1]
        self.rect.left=pos[0]
        self.viu = True
        self.final = True # per la animacio de morir
        self.change_x = 0
        self.change_y = 1
        self.world_shift = 0
        self.animacio = False

    def shift_world(self, shift_x):
                
        self.world_shift += shift_x
        self.rect.left += shift_x

    def update(self):
        if self.d == "left":
            self.llista_im = self.mat_l
        else:
            self.llista_im = self.mat_r
            
        if self.estat == self.ATTACK:
            self.count = self.count + 1
            if self.count == self.nframes * 4:
                self.count = 0
            fila = self.estat
            columna = self.count // 4
            if self.animacio:
                self.image = self.llista_im[fila][columna]
                self.image = pygame.transform.scale(self.image, (75, 75))


        elif self.estat == self.DIE:
            self.viu = False
            self.count = self.count + 1
            if self.count == self.nframes * 4:
                self.final = False
                self.kill()
            if self.final:
                fila = self.estat
                columna = self.count // 4
                if self.animacio:
                    self.image = self.llista_im[fila][columna]
                    self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect.left += self.change_x
        self.rect.top += self.change_y
        
        
    def canvia_estat(self, transicio=None):
        """Actualitza l'estat en funció de l'estat actual i de la transició

        """
        # En aquest cas, l'estat final és independent de l'estat
        # inicial: només depèn de la transició
        estat_anterior = self.estat
        if transicio == self.WAIT:
            self.estat = self.NO_ATTACK
        elif transicio == self.GO_ATTACK:
            self.estat = self.ATTACK
            self.animacio = True
        elif transicio == self.GO_DIE:
            self.estat = self.DIE
            self.animacio = True
        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))
        if self.estat != estat_anterior:
            self.count = 0
            
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -3
        self.d = "left"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 3
        self.d = "right"
        
    def stop(self):
        self.change_x = 0
        
    def grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 2 
