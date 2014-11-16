'''
Created on 16/nov/2014

@author: smonni
'''

from ln_core.resource_manager import ResourceManager 
import pygame
import random

class SoundManager:
    def __init__(self):
        self.rm = ResourceManager()
        pygame.mixer.init(44100, -16, 2, 1024)
    
    def get_sound(self,channel_index, sound_key, sound_key_index=-1):
        return Sound(channel_index, sound_key, sound_key_index)
    
    def get_music(self, sound_key, sound_key_index=-1):
        return Music(sound_key, sound_key_index)
    
    def get_playlist(self, channel_index, sound_keys_with_index):
        return SoundPlaylist(channel_index, sound_keys_with_index)
        
        
class Sound:
    def __init__(self, channel_index, sound_key, sound_key_index=-1):
        self.rm = ResourceManager()
        self.chan = pygame.mixer.Channel(channel_index)
        self.filename = self.rm.get_sound(sound_key, sound_key_index)
        self.file_to_play = pygame.mixer.Sound(self.filename)  
                      
    def play(self, repeat_count=0):
        self.chan.play(self.file_to_play, repeat_count)
    
    def fadeout(self, dur):
        self.chan.fadeout(dur)
        
    def stop(self):
        self.chan.stop()
        
    def set_volume(self, val):
        self.chan.set_volume(val)
      
class SoundPlaylist:
    def __init__(self, channel_index, sound_keys_with_index):
        self.rm = ResourceManager()
        self.channel_index = channel_index
        self.chan = pygame.mixer.Channel(channel_index)
        self.sound_keys_with_index = sound_keys_with_index
         
    def set_endevent(self, end_event):
        self.chan.set_endevent(end_event)
        
    def play(self, repeat_count=0):
        self.chan.play(self.file_to_play, repeat_count)
        
    def play_next_song(self, index=-1, repeat_count=0):
        print "play next song among:%s" % str(self.sound_keys_with_index)
        if index<0:
            index = random.randrange(0,len(self.sound_keys_with_index)-1)
        print "play next song:%s Type:%s" % (str(self.sound_keys_with_index[index]),
                                              str(type(self.sound_keys_with_index[index])))
                                             
        if ( len(self.sound_keys_with_index[index])>1 and type(self.sound_keys_with_index[index])==tuple):
            print "Soundkey %s is a tuple!" %  str(type(self.sound_keys_with_index[index]))
            sound_key_index = self.sound_keys_with_index[index][1]
            sound_key = self.sound_keys_with_index[index][0]
        else:
            print "Soundkey is not a tuple!"
            sound_key = self.sound_keys_with_index[index]
            sound_key_index = -1
            
        print "Channel:%s Sound Key: %s Sound Key Index: %s" % (self.channel_index, sound_key, sound_key_index)
        sound_to_play = Sound(self.channel_index, sound_key, sound_key_index)
        sound_to_play.play(repeat_count)
        #self.chan.play(sound_to_play, repeat_count)
    
    def fadeout(self, dur):
        self.chan.fadeout(dur)
        
    def stop(self):
        self.chan.stop()
        
    def set_volume(self, val):
        self.chan.set_volume(val)
    
    
class Music:
    def __init__(self, sound_key, sound_key_index=-1):
        self.rm = ResourceManager()
        self.filename = self.rm.get_sound(sound_key, sound_key_index)
        print "Loading bg music:%s" % self.filename
        pygame.mixer.music.load(self.filename)    
        
    def play(self, repeat_count=0):
        pygame.mixer.music.play(repeat_count)
    
    def stop(self):
        pygame.mixer.music.stop()
        
    def set_volume(self, val):
        pygame.mixer.music.set_volume(val)
        
        
        
    