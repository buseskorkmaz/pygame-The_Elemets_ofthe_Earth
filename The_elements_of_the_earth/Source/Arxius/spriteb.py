
import pygame
from Source.Arxius import conf
from Source.Arxius import nivells


class Animacio(pygame.sprite.Sprite):

    # Inicialitza els estats. Són nombres enters.
    LEFT, RIGHT =  1, 2
    # Inicialitza les transicions
    GO_LEFT, GO_RIGHT = range(2)

    def __init__(self, matriu_imatges, pos):
        super().__init__()
        # Defineix l'estat inicial
        self.estat = self.RIGHT
        self.llista_im = matriu_imatges
        self.count = 0
        self.nframes = len(self.llista_im[0])
        self.image = self.llista_im[self.estat][0]
        self.image=pygame.transform.scale(self.image,(50,100))
        self.rect = self.image.get_rect()
        self.rect.top=pos[1]
        self.rect.left=pos[0]
        self.change_x=0
        self.change_y=0
        self.prev = 0
        self.jumping = 0
        

    def update(self):
        self.count = self.count + 1
        if self.count == self.nframes * 5:
            self.count = 0
        fila = self.estat
        columna = self.count // 5
        if  self.change_x != 0 and self.jumping == 0:
            self.image = self.llista_im[fila][columna]
            self.image=pygame.transform.scale(self.image,(50,100))


            
        



    def canvia_estat(self, transicio=None):
        """Actualitza l'estat en funció de l'estat actual i de la transició

        """
        # En aquest cas, l'estat final és independent de l'estat
        # inicial: només depèn de la transició
        estat_anterior = self.estat
        if transicio == self.GO_RIGHT:
            self.estat = self.RIGHT
        elif transicio == self.GO_LEFT:
            self.estat = self.LEFT
    
        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))
        if self.estat != estat_anterior:
            self.count = 0
            
# Moviments
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
    def go_up(self):
        """ Called when the user hits the right arrow. """
        if self.jumping == 0:
            self.rect.y -= 1
            self.change_y = -20
            self.jumping = 1

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95

    def die(self):
        self.kill()
