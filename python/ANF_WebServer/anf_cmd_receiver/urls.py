'''
Created on 26/ott/2014

@author: smonni
'''
from django.conf.urls import patterns, url

from anf_cmd_receiver import views

urlpatterns = patterns('',
  # ex: /crib/
   
    url(r'^$', views.index, name='index'),  
     # ex: /crib/snow_on/
    url(r'^snow_on/$', views.snow_on, name='snow_on'),
    url(r'^snow_off/$', views.snow_off, name='snow_off'),
    url(r'^clouds_on/$', views.clouds_on, name='clouds_on'),
    url(r'^clouds_off/$', views.clouds_off, name='clouds_off'),
    url(r'^snow_balls_set_count/(?P<snow_ball_count>\d+)/$', views.snow_balls_set_count, name='snow_balls_set_count'),
    url(r'^cmd/(?P<cmd_name>\w+)/(?P<cmd_value>\w+)$', views.do_cmd, name='do_cmd'),
    
    url(r'^get_composite_cmds/$', views.get_composite_cmds, name='get_composite_cmds'),
    url(r'^get_scheduled_cmds/$', views.get_scheduled_cmds, name='get_scheduled_cmds'),
    
    url(r'^cmd_preset/(?P<preset_name>\w+)$', views.do_preset_cmd, name='do_preset_cmd'),
    
    url(r'^cmd_composite/(?P<cmd_key>\w+)$', views.do_composite_command_by_key, name='do_composite_command_by_key'),
     url(r'^cmd_scheduled/(?P<cmd_key>\w+)$', views.do_sheduled_commands_by_key, name='do_sheduled_commands_by_key')
)
