'''
Created on 06/dic/2012

@author: ubuntu
'''
import pygame
import random
import time


SCREENSIZE = 800, 480


class Rain(object):
    ' Rain generator'
    drops = []
    height = 10
    speed = 0.04
    color = (255, 255, 255, 255)
    chance = 0.5
    
    def __init__(self, **kwargs):
        ' Allow programmer to change settings of rain generator'
        self.__dict__.update(kwargs)


    def Render(self, screen):
        ' Render the rain'

        dirtyrects = []
        for drop in self.drops:
            drop.Render(dirtyrects, screen)
            if drop.dead:
                self.drops.remove(drop)
            else:
                dirtyrects.append(drop.rect)

        if random.random() < self.chance:
            for i in range(random.randrange(1,10)):
                self.drops.append(Rain.Drop(self.height, self.speed, self.color))
        return dirtyrects


    class Drop(object):
        ' Rain drop used by rain generator'
        pos = None
        dead = 0
        
        def __init__(self, height, speed, color):
            ' Initialize the rain drop'
            w, h = 3, int((random.randint(80, 120) * height) / 100.0)
            self.pic = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
            self.height = self.pic.get_height()
            self.maxy = SCREENSIZE[1] + h
            self.speed = speed
            self.pos = [random.random() * SCREENSIZE[0], -self.height]
            factor = float(color[3])/h
            r, g, b = color[:3]
            for i in range(h):
                self.pic.fill( (r, g, b, int(factor * i)), (1, i, w-2,1) )
                
            pygame.draw.circle(self.pic, (255, 255, 255), (1, h-2), 2)
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.pic.get_width(), self.pic.get_height())
            


        def Render(self, dirtyrects, screen):
            ' Draw the rain drop'
            self.pos[1] += self.speed
            self.rect.topleft = self.pos
            self.speed += .2
            if self.pos[1] > self.maxy:
                self.dead = 1
            else:
                screen.blit(self.pic, self.pos)


def main():

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE, 0, 32)


    # Create rain generator
    rain = Rain()


    # Main loop
    nexttime = time.time()
    ctr = 0
    quit = 0
    while not quit:
        # Uncomment the following line to make the rain go slower
        time.sleep(.01)
        # Track FPS

        if time.time() > nexttime:
            nexttime = time.time() + 1
            print '%d fps' % ctr
            ctr = 0

        ctr += 1
        
        # Draw rain

        dirtyrects = rain.Render(screen)
        
        # Update the screen for the dirty rectangles only
        pygame.display.update(dirtyrects)
        
        # Fill the background with the dirty rectangles only

        for r in dirtyrects:
            screen.fill((0, 0, 0), r)

        # Look for user quit
        pygame.event.pump()
        for e in pygame.event.get():
            if e.type in [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                quit = 1
                break


    # Terminate pygame
    pygame.quit()


if __name__ == "__main__":
    main()