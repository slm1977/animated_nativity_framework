'''
Created on 23/nov/2014

@author: smonni
'''

arduino_base_commands = {
              "LIGHT_ON" : (1,1,"A"),   # (PIN, VALUE)
              "LIGHT_ON_127" :(1,127,"A"),   # (PIN, VALUE,WRITE_MODE (A->Analog, D->Digital)
              "LIGHT_OFF" : (1,0,"D"),
              "FIRE_ON" : (2,1,"A"),   # (PIN, VALUE)
              "FIRE_OFF" : (2,0,"A"),
             
            }

anf_viewer_base_commands = {
                      "CLOUDS_OFF" :("CLOUDS_OFF",),
                      "CLOUDS_ON" : ("CLOUDS_ON",),
                      "SNOW_OFF" :("SNOW_OFF",),
                      "SNOW_ON" : ("SNOW_ON",),
                      "MANY_SNOW_FLICKS_ON" :("SNOW_FLICK_CHANGE_COUNT", 200)
                     }

composite_commands ={
                    "NIGHT" : ["LIGHT_ON", "FIRE_ON", "MANY_SNOW_FLICKS_ON"],
                    "DAY" : ["LIGHT_OFF", "FIRE_OFF"],
                    "NO_CLOUDS_NO_SNOW" : ["CLOUDS_OFF","SNOW_OFF"],
                    "CLOUDS_SNOW" : ["CLOUDS_ON","SNOW_ON"]
                    }


scheduled_commands=[(5,"NIGHT"), (10,"DAY")]

scheduled_commands2=[(5,"NO_CLOUDS_NO_SNOW"), (8,"CLOUDS_SNOW"), (20,"NO_CLOUDS_NO_SNOW"), (20,"NO_CLOUDS_NO_SNOW")]

from threading import Timer
from client_socket import SocketThread 
"""
Executes the command list
"""
def start_commands(scheduled_list):
    for l in scheduled_list:
        print "Creating timer for %s after %s seconds" % (l[1],l[0])
        t = Timer(l[0], send_command,args=[l[1]])
        t.start()


def send_command(composite_command):
    arduino_cmd,anf_cmd = format_composite_command(composite_command)
    print "Sending command %s to socket thread" % anf_cmd
    anfSocket = SocketThread(anf_cmd)



def get_arduino_commands_keys(command_key):
    if composite_commands.has_key(command_key):
        return  [k for k in composite_commands[command_key] if arduino_base_commands.has_key(k)]
    else:
        return [command_key]

def get_anf_player_commands_keys(command_key):
    if composite_commands.has_key(command_key):
        return  [k for k in composite_commands[command_key] if anf_viewer_base_commands.has_key(k)]
    else:
        return [command_key]

def format_base_command(cmd):
    target = base_commands[cmd][0]
    cmd_params = base_commands[cmd][1]
    
    if (target==CommandTarget.ARDUINO):
        cmd_to_send = format_base_arduino_command(cmd_params)
        
    elif (target==CommandTarget.ANF_VIEWER):
        cmd_to_send = format_base_anf_viewer_command(cmd_params)
    
    return cmd_to_send
    
    
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
    start_commands(scheduled_commands2)