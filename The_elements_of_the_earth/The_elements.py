# Character moves left/right falls down on a platform. With up key shots, p key pause and q key stop. After stop start with any key
 

# Pygame
import pygame
from pygame.locals import *

from sys import exit

# PGU
from pgu import engine

# Mòduls propis


from Source.Arxius import conf # Configuracions (imatges, posicions...)
from Source.Arxius import sprite_sheets # Per crear matrius de sprite sheets
from Source.Arxius import spriteb # Classe del personatge
from Source.Arxius import nivells # Classe de plataforma
from Source.Arxius.bala import Bala # Classe de bala
from Source.Arxius.selector import Selector # Classe per seleccionar al menu principal
from Source.Arxius import enemy1
from Source.Arxius import background


# Classe joc
class Joc(engine.Game):

    # Initialize screen, pygame modules, clock... and states.
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()
        self.pause = Pause(self)
        self.menu = Menu(self)
        self.gameover = Gameover(self)
        self.options = Options(self)

    # Creates and stores all states as attributes
    def _init_state_machine(self):
        self.jugant = Jugant(self)
    # Calls the main loop with the initial state.
    def run(self): 
        super().run(self.menu, self.screen)

   # Canviar a menu, pausa i jugar
    def change_state(self, transition=None):
        """
        Implements the automat for changing the state of the game.
        Given self.state and an optional parameter indicating 
        the kind of transition, computes and returns the new state
        """
        if self.state is self.menu:
            self.jugant.init()
            if transition == 'OPTIONS':
                new_state = self.options
            elif transition == 'PLAY':
                new_state = self.jugant

        elif self.state is self.options:
            if transition == 'EXIT':
                new_state = self.menu

        elif self.state is self.jugant:
            if transition == 'PAUSE':
                new_state = self.pause
            elif transition == 'EXIT':
                new_state = self.menu
            elif transition == 'GAMEOVER':
                new_state = self.gameover
            else:
                raise ValueError('Unknown transition indicator')

        elif self.state is self.pause:
            if transition == 'EXIT':
                new_state = self.menu
            elif transition == 'PLAY':
                new_state = self.jugant
            else:
                raise ValueError('Unknown transition indicator')

        elif self.state is self.gameover:
            if transition == 'EXIT':
                new_state = self.menu
            else:
                raise ValueError('Unknown transition indicator')

        else:
            raise ValueError('Unknown game state value')
        return new_state

     # Tick is called once per frame. It shoud control de timing.
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS


class Options(engine.State):

    def init(self):
        self.fons = conf.color_dead
    
    def paint(self, screen):
        screen.fill(self.fons)
        fons=pygame.image.load("Source/Imatges/instruccions.png").convert()
        screen.blit(fons,(0,0))
        pygame.display.flip()

    def event(self, event):
        if event.type is KEYDOWN:
            return self.game.change_state('EXIT')


class Gameover(engine.State):

    def init(self):
        self.fons = conf.color_dead
    
    def paint(self, screen):
        screen.fill(self.fons)
        fons=pygame.image.load("Source/Imatges/gameover.jpg").convert()
        screen.blit(fons,(120,130))
        pygame.display.flip()

    def event(self, event):
        if event.type is KEYDOWN:
            return self.game.change_state('EXIT')
    
# Classe menu
class Menu(engine.State):
    """
    Sample state game that admits a parameter on creation (an RGB color)
    """
    def init(self):
        self.all_sprites = pygame.sprite.Group()
        self.selector = Selector()
        self.all_sprites.add(self.selector)

    def paint(self,screen): 
        self.update(screen)
        
    def event(self,event):
       # if pygame.mouse.get_pressed():
        #    self.game.change_state('PLAY')
        if event.type is KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selector.up()
            elif event.key == pygame.K_RIGHT:
                self.selector.down()
            elif event.key == 13: # intro
                menu_sel = self.selector.select()
                if menu_sel == 0:
                    return self.game.change_state('PLAY')
                elif menu_sel == 1:
                    exit(0)
                elif menu_sel == 2:
                    return self.game.change_state('OPTIONS')
    def loop(self):
        self.all_sprites.update()

    # Update is called once a frame.  It should update the display.
    def update(self,screen):
        screen.fill((255,255,255))
        fons=pygame.image.load("Source/Imatges/pag_principal.png").convert()
        screen.blit(fons,(0,0))
        self.all_sprites.draw(screen)
        pygame.display.flip()

# Classe pausa
class Pause(engine.State):
    """
    A very boring state game: it shows nothing, only expects 'P' to be
    pressed!
    """
    def event(self,e): 
        if e.type is KEYDOWN and e.key == K_p:
            return self.game.change_state('PLAY')
        elif e.type is KEYDOWN and e.key == K_q:
            return self.game.change_state('EXIT')
        
    def paint(self, screen):
        fons=pygame.image.load(conf.fons_pausa).convert_alpha()
        screen.blit(fons,(120,70))
        pygame.display.flip()

        

# Classe del joc
class Jugant(engine.State):


    def init(self):

        #iniciem mixer
        pygame.mixer.pre_init()
        pygame.mixer.init()
        #iniciem musica principal

        self.musica=True
        if self.musica:
            pygame.mixer.music.load('Source/Sons/2.wav')
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)
            self.musica=False
            

        # Bala
        self.bales = pygame.sprite.Group()
        self.c_bala = 1
        im_bala_g = pygame.image.load(conf.s_bala_g)
        im_bala_b = pygame.image.load(conf.s_bala_b)
        self.lim_bales_g = sprite_sheets.crea_llista_imatges(im_bala_g, conf.n_im)
        self.lim_bales_b = sprite_sheets.crea_llista_imatges(im_bala_b, conf.n_im)

        # Plataforma
        
        self.platforms=nivells.Level_01()

        #enemy1
        self.enemics1 = self.platforms

        #Fons/Background
        self.world_shift_x=0
        self.background=self.platforms
        for fons in self.background.bg_list:
            fons.rect.left=fons.pos
            

        


        # Personatge
        im = pygame.image.load(conf.sprite_sheet_personatge)
        
        mat_im = sprite_sheets.crea_matriu_imatges(im, 4, 4)
        self.heroi = spriteb.Animacio( mat_im, conf.posicio_personatge)
        
        self.personatge = pygame.sprite.Group()
        self.personatge.add(self.heroi)


    def paint(self,screen):
        self.update(screen)

    def event(self,event):
        if event.type == KEYDOWN:
                
            # Moviment dreta i esquerra
            if event.key == pygame.K_RIGHT:
                self.heroi.canvia_estat(self.heroi.GO_RIGHT)
                self.heroi.go_right()
            elif event.key == pygame.K_LEFT:
                self.heroi.canvia_estat(self.heroi.GO_LEFT)
                self.heroi.go_left()
            elif event.key == pygame.K_UP:

                self.heroi.go_up()

            elif event.key == K_c:
                self.c_bala += 1

            # Disparar bala
            elif event.key == pygame.K_SPACE:
                #shotv = pygame.mixer.music.load('Source/Sons/lowRandom.mp3')
                #pygame.mixer.music.play()
                sound1 = pygame.mixer.Sound("Source/Sons/disparar.wav")
                pygame.mixer.find_channel().play(sound1)


                if self.c_bala % 2 == 0:
                    b = Bala(self.lim_bales_g, self.heroi.rect.center, self.heroi.estat,self.heroi.prev, "b")
                    if len(self.bales)<3:
                        self.bales.add(b)
                else:
                    b = Bala(self.lim_bales_b, self.heroi.rect.center, self.heroi.estat,self.heroi.prev, "r")
                    if len(self.bales)<3:
                        self.bales.add(b)

            # Pausa   
            elif event.key == K_p:
                return self.game.change_state('PAUSE')
            

        # Aturar el moviment del personatge    
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and self.heroi.change_x < 0) or (event.key == pygame.K_RIGHT and self.heroi.change_x > 0):
                self.heroi.stop()


    def loop(self):
        self.platforms.update_plat()

        #Heroi colisions
        self.personatge.update()
        
        if self.heroi.rect.top>conf.alçada_pantalla:
            return self.game.change_state('GAMEOVER')
        
        self.heroi.rect.left += self.heroi.change_x
        for p in self.platforms.platform_list:
            hit = self.heroi.rect.colliderect(p.rect)
            if hit:        
                self.heroi.rect.left -= self.heroi.change_x
                self.heroi.change_x = 0
        self.heroi.calc_grav()
        self.heroi.rect.top += self.heroi.change_y
        for p in self.platforms.platform_list:
            hit = self.heroi.rect.colliderect(p.rect)
            if hit:
                if self.heroi.change_y > 0:
                    self.heroi.rect.top = p.rect.top-100
                elif self.heroi.change_y < 0:
                    self.heroi.rect.top = p.rect.top+50

                self.heroi.change_y = 0
                self.heroi.jumping = 0

        #Bales colisions            
        self.bales.update()
        for bala in self.bales:
            for p in self.platforms.platform_list:
                hit = bala.rect.colliderect(p.rect)
                if hit:
                    bala.kill()

        
        self.platforms.update_ene()
        self.platforms.update_bg()

        #Scroll efect:
        diff=0

        if self.heroi.rect.left >= 500:
            diff = -self.heroi.rect.left + 500
            self.heroi.rect.left = 500
            
        if self.heroi.rect.left <= 300:
            diff = 300 - self.heroi.rect.left
            self.heroi.rect.left = 300
            
        self.platforms.shift_world(diff)
        self.world_shift_x +=diff
        
        for fons in self.platforms.bg_list:
            fons.world_shift(self.world_shift_x)

                
        


       #Enemies


    
        for enemy in self.platforms.enemy_list:
            
            enemy.shift_world(diff)
            if enemy.viu and abs(enemy.rect.top - self.heroi.rect.top) < 150:
                if abs(enemy.rect.left - self.heroi.rect.left) < 300:
                    if enemy.rect.left - self.heroi.rect.left > 0:
                        enemy.go_left()
                    elif enemy.rect.left - self.heroi.rect.left < -30:
                        enemy.go_right()
                    enemy.canvia_estat(enemy.GO_ATTACK)
                else:
                    enemy.canvia_estat(enemy.WAIT)

            enemy.grav()        
            enemy.rect.top += enemy.change_y
            for p in self.platforms.platform_list:
                hit = enemy.rect.colliderect(p.rect)
                if hit:
                    if enemy.change_y > 0:
                        enemy.rect.top = p.rect.top-75
                    enemy.change_y = 0
                    
            for bala in self.bales:
                if pygame.sprite.collide_rect(bala, enemy):
                    if bala.tipus == enemy.tipus:
                        enemy.stop()
                        enemy.canvia_estat(enemy.GO_DIE)
                    bala.kill()

            if pygame.sprite.collide_rect(self.heroi, enemy) and enemy.estat != enemy.DIE:
                self.heroi.die()
                return self.game.change_state('GAMEOVER')

      
            
            
    # Update is called once a frame.  It should update the display.
    def update(self,screen):
        self.platforms.draw_bg(screen)

        self.platforms.draw_ene(screen)
        self.platforms.draw_plat(screen)
        self.personatge.draw(screen)
        self.bales.draw(screen)
        
        pygame.display.flip()


# Programa principal
def main():
    game = Joc()
    game.run()
    
if __name__ == "__main__":
    main()
