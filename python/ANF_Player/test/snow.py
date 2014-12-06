'''
Created on 05/dic/2012

@author: ubuntu
'''
'''
Created on Sep 5, 2011

@author: Owner
'''
'''
Creates an animation of snowflakes falling against a night sky.
'''

import pygame
import random
import sys
from pygame.locals import FULLSCREEN



BACKGROUND_COLOR = (0, 0, 0)
SNOWFLAKE_COLOR = (255, 255, 255)

WINDOW_DIMENSIONS = [800, 800]

#window = pygame.display.set_mode(WINDOW_DIMENSIONS)
#pygame.display.set_caption("Snow Animation")

def get_snowflakes(xrange=800, yrange=800, num=120):
    snowflakes = [[random.randrange(0,xrange), random.randrange(0,yrange)]for i in range(num)]
    return snowflakes

def initialize_gui():
    ''' creates a window and sets the title'''
    screen_size = pygame.display.Info().current_w, pygame.display.Info().current_h
    window = pygame.display.set_mode(screen_size, FULLSCREEN)
    pygame.display.set_caption("Snow Animation")
    return window

def display_snowflakes(window,snowflakes):
    '''displays the snowflakes in the window'''
    
    window.fill(BACKGROUND_COLOR)
    
    for i in range (len(snowflakes)):
        pygame.draw.circle(window,SNOWFLAKE_COLOR,snowflakes[i],random.randrange(2,6))
        
   
        

clock = pygame.time.Clock()
done = False

def run(snowflakes, window, width=800):
    '''executes the animation loop to create a window and let the snow being'''
    
    display_snowflakes = snowflakes, window
    
    while not pygame.event.peek(pygame.QUIT):
        if pygame.event.peek(pygame.MOUSEBUTTONUP):
            display_snowflakes(snowflakes,window)
            pygame.event.clear()
            
        for event in pygame.event.get():   
            if (event.type == pygame.KEYDOWN):
                    if (event.key ==pygame.locals.K_q):  # quit
                        print "quitting"
                        done = True
                        pygame.event.clear()
        window.fill(BACKGROUND_COLOR)
        for i in range(len(snowflakes)):
            pygame.draw.circle(window,SNOWFLAKE_COLOR,snowflakes[i],random.randrange(2,6))
            snowflakes[i][1] += 1
            if snowflakes[i][1] > width:
                y = random.randrange(-50,-10)
                snowflakes[i][1] = y
                x = random.randrange(0,width)
                snowflakes[i][0] = x
                pygame.display.flip()
                    
                
 
    
    
def main(sysargs=None):
    pygame.init()
    snowflakes = get_snowflakes(1200,1200,400)
    window = initialize_gui()
    
    run(snowflakes, window,1200)
    
    clock.tick(60)
    pygame.quit()

if __name__=='__main__':
    main()



