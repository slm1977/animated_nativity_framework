'''
Created on 06/dic/2012

@author: ubuntu
'''

import pygame.locals

from meteo_core.meteo_sprites import Cloud, Background, SnowBall,ThunderBackground
from meteo_core.graphics_context import GC       
from pygame.locals import KEYDOWN, K_q
from meteo_core.server_socket import SocketThread

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
        self.gc = gc
        self.gc.set_fullscreen(False)
        self.snow_balls = []
        self.clouds =[]
        self.thunderBackground =ThunderBackground(self.gc)
        self.background =  Background(self.gc)
        self.snow_balls_count = 130
        self.create_snow_balls(self.snow_balls_count)
        self.create_clouds(3)
        self.thunder_on = True
        self.thunder_ts = 0
        self.init_sound()
        
        self.animals = []
        self.setup_animals_sounds()
        
        self.socketReceiver = SocketThread(self.on_data_received)
        self.socketReceiver.start()
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
            pygame.mixer.init(44100, -16, 2, 1024)
            
            pygame.mixer.music.load("res/suoni/Tu_scendi_dalle_stelle_2.mp3")
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            
            
            #pygame.mixer.init(11025, -16, 1, 1024)
            
            #sheep.fadeout(2000)
            people = pygame.mixer.Sound('res/suoni/people.wav')
#            gregge = pygame.mixer.Sound('res/suoni/windchimes_01.wav')
#            
#            chan_g = pygame.mixer.Channel(4)
#            chan_g.set_volume(0.0)
#            chan_g.play(gregge,-1)
            
            
            chan_p = pygame.mixer.Channel(6)
            chan_p.play(people,-1)
            chan_p.set_volume(0,5)
            
            #people.fadeout(2000)
            
            self.thunder = pygame.mixer.Sound('res/suoni/thunder.wav')
            self.thunder.set_volume(0.3)
            #thunder.play(-1)
            
            #fire = pygame.mixer.Sound('res/suoni/fire-burning.wav')
            #fire.set_volume(0.3)
            #fire.play(-1)
            
            #river = pygame.mixer.Sound('res/suoni/river2.wav')
            #river.set_volume(0.2)
            #river.play(-1)
            
            ululatoVento = pygame.mixer.Sound('res/suoni/UlulatoVento2.wav')
            ululatoVento.play(-1)
            
            self.cricket = pygame.mixer.Sound("res/suoni/CRICKET2.wav")
            self.cricket.play(-1)
            chan_c = pygame.mixer.Channel(5)
            chan_c.set_volume(0.3)
            chan_c.play(self.cricket,-1)
            
            
        except pygame.error, exc:
            print "Could not initialize sound system: %s" % exc
            sys.exit()
    
    def setup_animals_sounds(self):
        self.cow = pygame.mixer.Sound('res/suoni/cow.wav')
        #self.cow.fadeout(1200)
        self.dog = pygame.mixer.Sound('res/suoni/dog.wav')
        self.donkey = pygame.mixer.Sound('res/suoni/donkey.wav')
        #self.donkey.fadeout(2000)
        self.sheep = pygame.mixer.Sound('res/suoni/lamb3.wav')
        #self.sheep.fadeout(2300)
        
        
        self.animals.append(self.cow)
        self.animals.append(self.dog)
        self.animals.append(self.donkey)
        self.animals.append(self.sheep)
        
        self.animals_chan = []
        self.animals_chan.append(pygame.mixer.Channel(0))
        self.animals_chan[0].set_volume(0.4)
        self.animals_chan[0].set_endevent(MeteoViewer.EV_END_CHANNEL_0)
        
        self.animals_chan.append(pygame.mixer.Channel(1))
        self.animals_chan[1].set_volume(0.4)
        self.animals_chan[1].set_endevent(MeteoViewer.EV_END_CHANNEL_1)
       
        self.play_next_song(0) 
        self.play_next_song(1)         
    
    def play_next_song(self,num_chan):
        print "play next song!"
        next_sound = random.randrange(0,len(self.animals))
        self.animals_chan[num_chan].play(self.animals[next_sound], random.randint(0,1))
                   
#    def bela_pecora(self):
#        print "BELA PECORA"
#        self.chan = pygame.mixer.Channel(5)
#        self.chan.play(self.sheep)
#        #self.sheep.play()
#        self.chan.set_volume(0.8)
        

     
    def create_clouds(self, num=2):
        clouds = [".png","_2.png","_3.png"]
        
        for i in range(num):
            cim = "res/trasparent_cloud%s" % clouds[i%len(clouds)]
            cloud = Cloud(cim,self.gc.screen_w+(i+1)*10, random.randrange(50,200), -random.randrange(1,4),0)
            #nuvola.scalePercent(100)
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
            
        for n in self.clouds:
            n.move()
            
    
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
                    pygame.time.set_timer(MeteoViewer.EV_END_CHANNEL_0,0)
                    self.play_next_song(0)  
                elif (event.type==MeteoViewer.EV_PLAY_CHAN_1):
                    pygame.time.set_timer(MeteoViewer.EV_END_CHANNEL_1,0)
                    self.play_next_song(1)
                elif (event.type==MeteoViewer.EV_END_CHANNEL_0):
                    pygame.time.set_timer(MeteoViewer.EV_PLAY_CHAN_0, random.randrange(2500,6000))
                elif (event.type==MeteoViewer.EV_END_CHANNEL_1):
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
    
    