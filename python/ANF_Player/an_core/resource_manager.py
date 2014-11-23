'''
Created on 16/nov/2014

@author: smonni
'''

import os.path, random

class ImageKey:
    CLOUD = "CLOUD"
    SNOW_BALL = "SNOW_BALL"
    RAIN_DROP = "RAIN_DROP"
    
class BackgroundKey:
    BACKGROUND_NIGHT = "BACKGROUND_NIGHT"
    BACKGROUND_NIGHT_THUNDER = "BACKGROUND_NIGHT_THUNDER"
    
class SoundKey:
    BACKGROUND_MUSIC = "BACKGROUND_MUSIC"
    BACKGROUND_NIGHT_THUNDER = "BACKGROUND_NIGHT_THUNDER"
    COW = "COW"
    CRICKET = "CRICKET"
    DOG = "DOG"
    DONKEY = "DONKEY"
    LAMB = "LAMB"
    SHEEP= "SHEEP"
    PEOPLE = "PEOPLE"
    WIND_CHIMES = "WIND_CHIMES"
    RIVER = "RIVER"
    FIRE = "FIRE"
    THUNDER = "THUNDER"
    WIND = "WIND"
    DOG = "DOG" 
     
                
image_object_path_dict = {  "CLOUD" : ["transparent_cloud.png",
                                       "transparent_cloud_2.png",
                                       "transparent_cloud_3.png"],
                            "SNOW_BALL" : ["snowflick.png"],
                            
                            "RAIN_DROP" : ["goccia_001_jpg"]
                             
             }

image_background_path_dict = {
                               "BACKGROUND_NIGHT" : ["cielo_stellato_cometa.jpg"],
                               "BACKGROUND_NIGHT_THUNDER" : ["cielo_stellato_cometa_2.jpg"]
                              }

sound_path_dict = {
                   
                   # background music
                   "BACKGROUND_MUSIC" :  ["Tu_scendi_dalle_stelle.mp3", "Tu_scendi_dalle_stelle_2.mp3"],
                   
                   # people, animals and other "human" sound effects
                   "COW" : ["cow.wav"],
                   "CRICKET": ["cricket.wav"],
                   "DONKEY": ["donkey.wav"],
                   "DOG" : ["dog.wav"],
                   "LAMB" : ["lamb.wav"],
                   "SHEEP" : ["sheep.wav"],
                   "PEOPLE" : ["people.wav"],
                   "WIND_CHIMES" : ["windchimes_01.wav"],
                   
                   # weather effects
                   "RIVER" : ["river2.wav"],
                   "FIRE" : ["fire_burning.wav"],
                   "THUNDER" : ["Lightning.wav", "thunder.mp3"],
                   "WIND" : ["UlulatoVento.wav"]
                   }

class ResourcePath:
    IMAGE_BACKGROUD = ["backgrounds", image_background_path_dict]
    SOUND =  ["sounds" , sound_path_dict]
    IMAGE_OBJECT= ["images", image_object_path_dict]

        
class ResourceManager:
    def __init__(self, root_path = "../res"):
        self.root_path = root_path
    
    def get_resource(self, res_type, res_key, res_index=0):
        if res_index<0:
            res_index = random.randint(0, len(res_type[1][res_key])-1)
             
        res_name = res_type[1][res_key][res_index]
        res_path = os.path.join(self.root_path,res_type[0],res_name)
        
        return res_path       
     
    def get_sound(self,sound_key, sound_index=0):
        return self.get_resource(ResourcePath.SOUND, sound_key, sound_index)
    
    def get_background(self,bg_key, bg_index=0):
        return self.get_resource(ResourcePath.IMAGE_BACKGROUD, bg_key, bg_index)
    
    def get_image(self,key,index=0):
        return self.get_resource(ResourcePath.IMAGE_OBJECT, key, index)
    
    def get_resource_keys(self,resource_type):
        return resource_type[1].keys()
    
    def get_resources_path(self,resource_type):
        return os.path.join(self.root_path,  resource_type[0])
          

if __name__=="__main__":
    rm = ResourceManager()
    print "Cloud 1:%s" % rm.get_image(ImageKey.CLOUD, -1)
    print "Cloud 1:%s" % rm.get_image(ImageKey.CLOUD, -1)
    print "Cloud 1:%s" % rm.get_image(ImageKey.CLOUD, -1)
    print "Object lists Dir:%s" % rm.get_resources_path(ResourcePath.IMAGE_OBJECT)
    print "Object lists:%s" % rm.get_resource_keys(ResourcePath.IMAGE_OBJECT)
    print "Sound lists:%s" % rm.get_resource_keys(ResourcePath.SOUND)
    print "River Path:%s" % rm.get_sound("RIVER")
    print "Snow ball Path:%s" % rm.get_image("SNOW_BALL")
    print "Random River Path:%s" % rm.get_sound("RIVER",-1)
    print "BG:%s" % rm.get_background("BACKGROUND_NIGHT",0)
                        