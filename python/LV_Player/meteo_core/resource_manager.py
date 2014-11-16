'''
Created on 16/nov/2014

@author: smonni
'''

import os.path, random



image_object_path_dict = {  "CLOUD" : ["transparent_cloud.png",
                                       "transparent_cloud_2.png",
                                       "transparent_cloud_3.png"],
                            "SNOW_BALL" : ["snowflick.png"],
                            
                            "RAIN_DROP" : ["goccia_001_jpg"]
                             
             }

image_background_path_dict = {
                               "BACKGROUND_NIGHT" : ["cielo_stellato_cometa.png"],
                               "BACKGROUND_NIGHT_THUNDER" : ["cielo_stellato_cometa_2.png"]
                              }

sound_path_dict = {
                   
                   # background music
                   "BACKGROUND_MUSIC" :  ["Tu_scendi_dalle_stelle.mp3", "Tu_scendi_dalle_stelle_2.mp3"],
                   
                   # people, animals and other "human" sound effects
                   "COW" : ["cow.wav"],
                   "CRICKET": ["cricket.wav"],
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
        print "res path key:%s" % res_type[0]
        if res_index<0:
            print "index<0"
            res_index = random.randint(0, len(res_type[1][res_key])-1)
            print "res_index set to:%d" % res_index
       
        res_name = res_type[1][res_key][res_index]
        res_path = os.path.join(self.root_path,res_type[0],res_name)
        
        return res_path       
     
    def get_sound(self,sound_key, sound_index=0):
        print "RR:%s" % ResourcePath.SOUND
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
    print "Object lists Dir:%s" % rm.get_resources_path(ResourcePath.IMAGE_OBJECT)
    print "Object lists:%s" % rm.get_resource_keys(ResourcePath.IMAGE_OBJECT)
    print "Sound lists:%s" % rm.get_resource_keys(ResourcePath.SOUND)
    print "River Path:%s" % rm.get_sound("RIVER")
    print "Snow ball Path:%s" % rm.get_image("SNOW_BALL")
    print "Random River Path:%s" % rm.get_sound("RIVER",-1)
    print "BG:%s" % rm.get_background("BACKGROUND_NIGHT",0)
                        