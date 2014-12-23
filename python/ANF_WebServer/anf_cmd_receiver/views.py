
from django.http import HttpResponse
from anf_cmd_receiver import client_socket, command_manager 

import json

def index(request):
    return HttpResponse("Welcome to the Animated Nativity Framework Server Manager!!")

 
def snow_on(request):
    client_socket.SocketThread("SNOW_ON")
    return HttpResponse("SNOW ON REQUEST SENT!")

def snow_off(request):
    client_socket.SocketThread("SNOW_OFF")
    return HttpResponse("SNOW OFF REQUEST SENT!")

def clouds_on(request):
    client_socket.SocketThread("CLOUDS_ON")
    return HttpResponse("CLOUDS_ON REQUEST SENT!")

def clouds_off(request):
    client_socket.SocketThread("CLOUDS_OFF")
    return HttpResponse("CLOUDS_OFF REQUEST SENT!")

def light_on(request):
    client_socket.BT_SocketThread("led_on")
    return HttpResponse("LED ON REQUEST SENT!")

def light_off(request):
    BT_SocketThread("led_off")
    return HttpResponse("LED OFF REQUEST SENT!")


def snow_balls_set_count(request, snow_ball_count):
    cmd = "SNOW_FLICK_CHANGE_COUNT|%s" % snow_ball_count
    client_socket.SocketThread(cmd)
    return HttpResponse("%s COMMAND SENT!" % cmd)

def get_composite_cmds(request):
    cmds = command_manager.get_available_composite_commands()
    return HttpResponse(json.dumps(cmds))

def get_scheduled_cmds(request):
    cmds = command_manager.get_available_scheduled_commands()
    
    return HttpResponse(json.dumps(cmds))

def do_composite_command_by_key(request, cmd_key):
    command_manager.do_composite_command_by_key(cmd_key)
    return HttpResponse("COMPOSITE COMMAND SENT FOR KEY:%s" % cmd_key)

def do_sheduled_commands_by_key(request, cmd_key):
    command_manager.do_scheduled_commands_by_key(cmd_key)
    return HttpResponse("SCHEDULED COMMAND SENT FOR KEY:%s" % cmd_key)

def do_cmd(request, cmd_name, cmd_value):
    return HttpResponse("Command: %s Value:%s" % (cmd_name, cmd_value) )

def do_preset_cmd(request, preset_name):
    return HttpResponse("Preset Command: %s " % preset_name)
    