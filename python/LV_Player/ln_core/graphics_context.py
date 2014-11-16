import pygame
from pygame.locals import FULLSCREEN

class GC(object):
    def __init__(self):
         
        pygame.display.init()
        self.background_color = (0, 0, 0)
        self.screen_size = self.screen_w, self.screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h
        #self.screen = pygame.display.set_mode(self.screen_size, FULLSCREEN)
        #SCREENSIZE = (640, 480)
        self.screen = pygame.display.set_mode(self.screen_size)
        
        pygame.font.init()
        pygame.mouse.set_visible(True)
        pygame.key.set_repeat(600, 100)
        self.font10 = pygame.font.Font(None, 10)
        self.font12 = pygame.font.Font(None, 12)
        self.font14 = pygame.font.Font(None, 14)
        self.font16 = pygame.font.Font(None, 16)
        self.font18 = pygame.font.Font(None, 18)
        self.font20 = pygame.font.Font(None, 20)
        self.font22 = pygame.font.Font(None, 22)
        self.font24 = pygame.font.Font(None, 24)
        self.font32 = pygame.font.Font(None, 32)
    
    def set_fullscreen(self, val):
        if val:
            self.screen = pygame.display.set_mode(self.screen_size, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)
            
        
     
