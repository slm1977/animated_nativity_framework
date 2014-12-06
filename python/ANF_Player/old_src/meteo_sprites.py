'''
Created on 06/dic/2012

@author: ubuntu
'''
import pygame
import random
from Crypto.Random.random import randint

class ElementSprite(pygame.sprite.Sprite):
    image = None
    
    def __init__(self, cls, img_path = None):
      
        pygame.sprite.Sprite.__init__(self)

        if cls.image is None:
            # This is the first time this class has been instantiated.
            # So, load the image for this and all subsequence instances.
            if img_path is not None:
                cls.image = pygame.image.load(img_path)
            else:
                cls.image = pygame.Surface([15, 15])
                #cls.image = pygame.image.load(img_path)
                
        self.image = cls.image #CarrierSprite.image.convert(CarrierSprite.image)
        self.rect = self.image.get_rect()
        self.x = self.rect[0]
        self.y = self.rect[1]
                
    def draw(self,gc):
        #self.rect.center = (self.element.position, self.element.position)
        gc.screen.blit(self.image, self.rect)
    
    def scalePercent(self,perc):
        size_x = int(self.rect.width*perc/100.0)
        size_y = int(self.rect.height*perc/100.0)
        print "SIZE:%s,%s" % (size_x,size_y)
        self.image = pygame.transform.scale(ElementSprite.image, (size_x, size_y))
        self.rect = self.image.get_rect() 
        print "dopo di scale:%s" % self.rect.width
    
            
    
    
    def update_position(self, x,y):
        if x:
            self.rect[0] = x
            self.x = x
        if y:
            self.rect[1] = y
            self.y = y
        
    
  

class Background(ElementSprite):
    image = None
    def __init__(self, gc):
        ElementSprite.__init__(self, self.__class__, "res/sfondi/cielo_stellato_cometa.jpg")
        self.image = pygame.transform.scale(self.image, (gc.screen_w, gc.screen_h))

class ThunderBackground(ElementSprite):
    image = None
    def __init__(self,gc):
        ElementSprite.__init__(self, self.__class__, "res/sfondi/cielo_stellato_cometa_2.jpg")   
        self.image = pygame.transform.scale(self.image, (gc.screen_w, gc.screen_h))
        
class Cloud(ElementSprite):
    image = None
    def __init__(self,file_name, x,y, speed_x, speed_y=0):
        ElementSprite.__init__(self, self.__class__,file_name)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.start_x = x
        self.fx = x
        self.update_position(x, y)
        
        
    def move(self):
        self.fx = self.fx + self.speed_x    
        if self.fx< - self.rect.width:
            self.fx = self.start_x
        
        self.y = self.y + randint(-1,1)*randint(0,1)
        self.update_position(round(self.fx),self.y)
        
       

class SnowBall(ElementSprite):
    image = None
    def __init__(self, x=0, y=0, speed_x=0, speed_y = 0, swing_tick=10):
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        self.swing_tick= swing_tick
        self.swing_val = 0
        self.go_right = True
        
        ElementSprite.__init__(self, self.__class__,"res/snowflick.png")
        self.update_position(x, y)
        
    def scaleSprite(self,size):
        self.image = pygame.transform.smoothscale(SnowBall.image, (size, size))
        self.rect = self.image.get_rect() 
        self.scale = size
    
   
        
    def go_down(self):
        self.swing_val = random.random()
        
        if self.swing_val<0.05:
            self.go_right = not self.go_right
        if self.go_right:
            x_pos = self.x + self.speed_x 
        else:
            x_pos = self.x - self.speed_x   
                
        self.update_position(x_pos, self.y+ self.speed_y)  