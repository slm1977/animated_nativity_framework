
from django.http import HttpResponse
from client_socket import ClientSocket, BT_ClientSocketThread

def index(request):
    return HttpResponse("Welcome to the Animated Nativity Framework Server Manager!!")

 
def snow_on(request):
    ClientSocket("SNOW_ON")
    return HttpResponse("SNOW ON REQUEST SENT!")

def snow_off(request):
    ClientSocket("SNOW_OFF")
    return HttpResponse("SNOW OFF REQUEST SENT!")

def clouds_on(request):
    ClientSocket("CLOUDS_ON")
    return HttpResponse("CLOUDS_ON REQUEST SENT!")

def clouds_off(request):
    ClientSocket("CLOUDS_OFF")
    return HttpResponse("CLOUDS_OFF REQUEST SENT!")

def light_on(request):
    BT_ClientSocketThread("led_on")
    return HttpResponse("LED ON REQUEST SENT!")

def light_off(request):
    BT_ClientSocketThread("led_off")
    return HttpResponse("LED OFF REQUEST SENT!")


def snow_balls_set_count(request, snow_ball_count):
    cmd = "SNOW_FLICK_CHANGE_COUNT|%s" % snow_ball_count
    ClientSocket(cmd)
    return HttpResponse("%s COMMAND SENT!" % cmd)

def do_cmd(request, cmd_name, cmd_value):
    return HttpResponse("Command: %s Value:%s" % (cmd_name, cmd_value) )

def do_preset_cmd(request, preset_name):
    return HttpResponse("Preset Command: %s " % preset_name)
    