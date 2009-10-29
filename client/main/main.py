# -*- coding: utf-8 -*-
import thread
import time
import sys

if sys.version_info[1] == 3:
    print "nu glömde du skriva python2.5... trooooooliiiigt"
    sys.exit(0)

import dbus, dbus.glib, dbus.service

import gui_thread

import data
#from dbus.mainloop.glib import DBusGMainLoop
#import gobject
print "före hax"
#dbus_loop = DBusGMainLoop(set_as_default=True)

print  "efter hax"

#bus = dbus.SessionBus(mainloop=dbus_loop)
print "efter bus"
#proxy = bus.get_object("rad.main",
#		"/rad/main/echo")

print "efter proxy"
gui_thread.run()
print "efter map_thread"

#loop = gobject.MainLoop()
print "mloop"
#thread.start_new_thread(loop.run, tuple())
print "DONEloop"
