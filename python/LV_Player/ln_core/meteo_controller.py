'''
Created on 06/dic/2012

@author: ubuntu
'''

import pygame.locals

from ln_core.sprites import Cloud, Background, SnowBall,ThunderBackground
from ln_core.sounds import SoundManager 
from ln_core.resource_manager import SoundKey

from ln_core.graphics_context import GC       
from pygame.locals import KEYDOWN, K_q
from ln_core.comm.server_socket import SocketThread

import random
import time
import sys

class MeteoViewer:
    EV_END_CHANNEL_0 = pygame.locals.USEREVENT+1
    EV_END_CHANNEL_1 = pygame.locals.USEREVENT+2
    
    EV_PLAY_CHAN_0 = pygame.locals.USEREVENT+3
    EV_PLAY_CHAN_1 = pygame.locals.USEREVENT+4
    
    
# STATES 
    SNOW_ON = True
    CLOUDS_ON = True
    
    
    def __init__(self,gc):
        print "Meteo Viewer Editor"
        self.gc = gc
        # set or unset fullscreen mode
        self.gc.set_fullscreen(False)
        
        self.snow_balls = []
        self.clouds =[]
        
        self.thunderBackground = ThunderBackground(self.gc)
        self.background =  Background(self.gc)
        
        self.clouds_count = 10
        self.snow_balls_count = 130
        
        
        self.create_snow_balls(self.snow_balls_count)
        self.create_clouds(self.clouds_count )
        self.thunder_on = True
        self.thunder_ts = 0
        self.init_sound()
       
        self.setup_animals_sounds_playlist()
        
        #self.socketReceiver = SocketThread(self.on_data_received)
        #self.socketReceiver.start()
        
        self.run()
        
    def on_data_received(self, data):
        print "Data received from the client:%s" % data
        data = self.parse_data(data)
        if (data[0]=="SNOW_ON"):
            MeteoViewer.SNOW_ON = True
        elif (data[0]=="SNOW_OFF"):
            MeteoViewer.SNOW_ON = False
        if (data[0]=="CLOUDS_ON"):
            MeteoViewer.CLOUDS_ON = True
        elif (data[0]=="CLOUDS_OFF"):
            MeteoViewer.CLOUDS_ON = False
        elif (data[0]=="SNOW_FLICK_CHANGE_COUNT"):
            self.snow_balls_count = int(data[1])
            
    def parse_data(self, data):
        return data.split("|")
        
        
    def init_sound(self):
        # sounds
        try:
            self.sound_manager = SoundManager()
            self.music = self.sound_manager.get_music(SoundKey.BACKGROUND_MUSIC,1)
            self.music.set_volume(1.0)
            self.music.play(-1)
            
             
            #sheep.fadeout(2000)
            people = self.sound_manager.get_sound(6, SoundKey.PEOPLE)
            people.play(-1)
            people.set_volume(0.5)
            #people.fadeout(2000)
            
            self.thunder = self.sound_manager.get_sound(4, SoundKey.THUNDER)
            self.thunder.set_volume(0.3)
            
           
        except pygame.error, exc:
            print "Could not initialize sound system: %s" % exc
            sys.exit()
    
    def setup_animals_sounds_playlist(self):
        
        self.animal_sounds = [SoundKey.COW, (SoundKey.SHEEP,-1), SoundKey.LAMB]
       
        self.playlist_1 = self.sound_manager.get_playlist(0, self.animal_sounds)
        self.playlist_1.set_endevent(MeteoViewer.EV_END_CHANNEL_0)
       
        self.playlist_2 = self.sound_manager.get_playlist(1, self.animal_sounds)
        self.playlist_2.set_endevent(MeteoViewer.EV_END_CHANNEL_1)
        
        self.play_next_song(0)
        self.play_next_song(1)

    def play_next_song(self,num_chan):
        print "play next song!"
        if num_chan==0:
            self.playlist_1.play_next_song(-1, random.randint(0,1))
        elif num_chan==1:  
            self.playlist_2.play_next_song(-1, random.randint(0,1))
            
        
    def create_clouds(self, num=2):
         
        for i in range(num):
            
            cloud = Cloud(-1,self.gc.screen_w+(i+1)*10, random.randrange(80,200), -random.randrange(1,5), random.randrange(-2,2))
            cloud.scalePercent(random.randrange(50,100))
            self.clouds.append(cloud)
        
        
        
    def create_snow_balls(self, num=100, y0=None):
        y0_to_set = (y0==None)
        for i in range(num):
            x0 = random.randrange(0, self.gc.screen_w)
            if y0_to_set:
                y0 = random.randrange(-self.gc.screen_h, 0)
            speed_x = 1
            speed_y = random.randrange(5, 10)
            
            pn = SnowBall(x0,y0, speed_x,speed_y)
            pn.scaleSprite(random.randrange(5,10))
            self.snow_balls.append(pn)  
        
      
    
    def update_positions(self):
        for sn in self.snow_balls:
            sn.go_down()
            
        for c in self.clouds:
            c.move()
            
    
    def check_for_regeneration(self):
        num_rem = 0
        for pn in self.snow_balls:
            if pn.y+ 10 > self.gc.screen_h:
                self.snow_balls.remove(pn)
                num_rem +=1
        
        self.create_snow_balls(self.snow_balls_count - len(self.snow_balls))
        
    def play_thunder(self): 
      
        v = random.random()
        if v<0.6:
            self.background.draw(self.gc)  
        else:
            self.thunderBackground.draw(self.gc) 
                
        if time.time()-self.thunder_ts>4:
            self.thunder_on = False 
              
    def draw(self):
        
        pygame.draw.rect(self.gc.screen,self.gc.background_color, (0, 0,self.gc.screen_w, self.gc.screen_h)) # clear screen
        
        if not self.thunder_on:
            r = random.random()
            if r < 0.003:
                self.thunder_ts =time.time()
                self.thunder_on = True
                self.thunder.play()
        
        if self.thunder_on:
            self.play_thunder()
        else:
            self.background.draw(self.gc) 
            
        if MeteoViewer.SNOW_ON: 
            for sn in self.snow_balls:
                sn.draw(self.gc)
                
        
        if MeteoViewer.CLOUDS_ON:       
            for n in self.clouds:
                n.draw(self.gc)
            
        pygame.display.update()
               
    def run(self):
        print "Running meteo controller"
        done = False
        x = 0
        y = 0
        while not done:
            for event in pygame.event.get():
                if (event.type==MeteoViewer.EV_PLAY_CHAN_0):
                    print "EV_PLAY_CHAN_0!!"
                    pygame.time.set_timer(MeteoViewer.EV_END_CHANNEL_0,0)
                    self.play_next_song(0)  
                elif (event.type==MeteoViewer.EV_PLAY_CHAN_1):
                    print "EV_PLAY_CHAN_1!!"
                    pygame.time.set_timer(MeteoViewer.EV_END_CHANNEL_1,0)
                    self.play_next_song(1)
                elif (event.type==MeteoViewer.EV_END_CHANNEL_0):
                    print ".EV_END_CHANNEL_0!!"
                    pygame.time.set_timer(MeteoViewer.EV_PLAY_CHAN_0, random.randrange(2500,6000))
                elif (event.type==MeteoViewer.EV_END_CHANNEL_1):
                    print ".EV_END_CHANNEL_1!!"
                    pygame.time.set_timer(MeteoViewer.EV_PLAY_CHAN_1, random.randrange(2500,6000))
                    
                if (event.type == KEYDOWN):
                    if (event.key == K_q):  # quit
                        print "quitting"
                        done = True
                        pygame.event.clear()
                      
            self.update_positions()
            self.draw()
            self.check_for_regeneration()
            time.sleep(0.01)
        
            
           
             

if __name__=='__main__':
    gc = GC()
    mv = MeteoViewer(gc)
    
    