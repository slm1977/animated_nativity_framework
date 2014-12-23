'''
Created on 23/nov/2014

@author: smonni
'''

ANF_COMMANDS_ON = True   # enable sending command to the ANF Viewer
ARDUINO_COMMANDS_ON = False  # enable sending command to the BT Arduino Controller

class Command:
    CLOUDS_OFF = "CLOUDS_OFF"
    CLOUDS_ON = "CLOUDS_ON"
    SCREEN_OFF = "SCREEN_OFF"
    SCREEN_ON = "SCREEN_ON"
    SNOW_OFF = "SNOW_OFF"
    SNOW_ON = "SNOW_ON"
    SOUNDS_OFF = "SOUNDS_OFF"
    SOUNDS_ON = "SOUNDS_ON"
    SNOW_FLICK_COUNT_CHANGE = "SNOW_FLICK_CHANGE_COUNT"
    
    

arduino_base_commands = {
              "LIGHT_ON" : (1,1,"A"),   # (PIN, VALUE)
              "LIGHT_ON_127" :(1,127,"A"),   # (PIN, VALUE,WRITE_MODE (A->Analog, D->Digital)
              "LIGHT_OFF" : (1,0,"D"),
              "FIRE_ON" : (2,1,"A"),   # (PIN, VALUE)
              "FIRE_OFF" : (2,0,"A"),
             
            }

anf_viewer_base_commands = {
                      Command.CLOUDS_OFF :(Command.CLOUDS_OFF,),
                      Command.CLOUDS_ON : (Command.CLOUDS_ON,),
                      Command.SNOW_OFF:(Command.SNOW_OFF,),
                      Command.SNOW_ON : (Command.SNOW_ON,),
                      Command.SNOW_ON : (Command.SNOW_ON,),
                      Command.SCREEN_OFF:(Command.SCREEN_OFF,),
                      Command.SCREEN_ON:(Command.SCREEN_ON,),
                      Command.SOUNDS_OFF:(Command.SOUNDS_OFF,),
                      Command.SOUNDS_ON:(Command.SOUNDS_ON,),
            
                      "MANY_SNOW_FLICKS_ON" :(Command.SNOW_FLICK_COUNT_CHANGE, 200)
                     }

composite_commands ={
                    "NO_SOUND_NO_VIDEO" : [Command.SCREEN_OFF, Command.SOUNDS_OFF],
                    "ONLY_AUDIO" : [Command.SCREEN_OFF, Command.SOUNDS_ON],
                    "NIGHT" : ["LIGHT_ON", "FIRE_ON", "MANY_SNOW_FLICKS_ON"],
                    "DAY" : ["LIGHT_OFF", "FIRE_OFF"],
                    "NO_CLOUDS_NO_SNOW" : [Command.SCREEN_ON, Command.CLOUDS_OFF, Command.SNOW_OFF],
                    "CLOUDS_SNOW" : [Command.SCREEN_ON, Command.CLOUDS_ON,Command.SNOW_ON]
                    }


scheduled_commands=  { "NIGHT_AND_DAY " :[(5,"NIGHT"), (10,"DAY")],
                       "SCENE_OFF_TO_SCENE_ON" : [(0, "NO_SOUND_NO_VIDEO"), #(5,"ONLY_AUDIO"),
                                                  (10,"NO_CLOUDS_NO_SNOW"),  (15, Command.SNOW_ON), 
                                                  (20,"NO_CLOUDS_NO_SNOW"), (20,"NO_CLOUDS_NO_SNOW")]
                      }



from threading import Timer
from client_socket import SocketThread, BT_ClientSocketThread


def get_available_composite_commands():
    return composite_commands.keys()

def get_available_scheduled_commands():
    return scheduled_commands.keys()

def do_composite_command_by_key(key):
    send_command(key)
    
def do_scheduled_commands_by_key(key):
    start_commands(scheduled_commands[key])
    
def start_commands(scheduled_list):
    """
    Executes the sheduled command list (each element contains a tuple (<delay_time_in_seconds>, <composite_command_key>)
    """
    for l in scheduled_list:
        print "Creating timer for %s after %s seconds" % (l[1],l[0])
        t = Timer(l[0], send_command,args=[l[1]])
        t.start()


def send_command(composite_command):
    """
    Execute a composite_command. i.e a list of elements such as [<composite_cmd_key1>,<composite_cmd_key2> ...]
    """
    
    print "Called send command for:%s"  % str(composite_command)
    arduino_cmd,anf_cmd = format_composite_command(composite_command)
    
    if ANF_COMMANDS_ON:
        print "Sending ANF command %s to socket thread" % anf_cmd
        anfSocket = SocketThread(anf_cmd)
    if ARDUINO_COMMANDS_ON:
        print "Sending BT command %s to BT socket thread" % arduino_cmd
        arduinoSocket = BT_ClientSocketThread(arduino_cmd)



def get_arduino_commands_keys(command_key):
    if composite_commands.has_key(command_key):
        return  [k for k in composite_commands[command_key] if arduino_base_commands.has_key(k)]
    else:
        if arduino_base_commands.has_key(command_key):
            return [command_key]
        else:
            return []

def get_anf_player_commands_keys(command_key):
    if composite_commands.has_key(command_key):
        return  [k for k in composite_commands[command_key] if anf_viewer_base_commands.has_key(k)]
    else:
        if anf_viewer_base_commands.has_key(command_key):
            return [command_key]
        else:
            return []
    
def format_base_arduino_command(cmd):
    params = arduino_base_commands[cmd]
    print "Format Base arduino command %s:  params:%s" % (cmd,str(params))
    
    return "%s%s,%s" % (params[2],params[0],params[1])  # D1,0 (digital pin 1 to 0 value)

def format_base_anf_viewer_command(cmd):
    
    cmd_params = anf_viewer_base_commands[cmd]
    print "Format Base ANF viewer command %s:  params:%s" % (cmd,str(cmd_params))
    comp_cmd = ""
    for p in cmd_params:
        comp_cmd+= str(p) + ","
    return comp_cmd[:-1] 


def format_composite_command(key):
    arduino_cmd_list = get_arduino_commands_keys(key)
    anf_cmd_list = get_anf_player_commands_keys(key)
    anf_command = ""
    arduino_command =""

    print "Arduino Command List:%s" % arduino_cmd_list
    print "Anf Player Command List:%s" % anf_cmd_list
    for cmd in arduino_cmd_list:
        print "CMD:%s" % cmd
        arduino_command+= format_base_arduino_command(cmd) + "|"
    
 
    for cmd in anf_cmd_list:
        print "CMD:%s" % cmd
        anf_command+= format_base_anf_viewer_command(cmd) + "|"
        
    return [arduino_command[:-1],anf_command[:-1]]
 
if __name__=='__main__':
    #print "NIGHT COMMAND:%s" % format_composite_command("NIGHT")
    start_commands(scheduled_commands["SCENE_OFF_TO_SCENE_ON"])
    