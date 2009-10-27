# -*- coding: utf-8 -*-
import thread
import time
import sys

if sys.version_info[1] == 3:
    print "nu glömde du skriva python2.5... trooooooliiiigt"
    sys.exit(0)

import dbus
import map_thread

bus = dbus.SessionBus()

map_thread.run()

