# Example code for use of liblocation wrapper. 
#
# Copyright 2008 by Robert W. Brewer.  < rwb123 at gmail dot com >
# This file is placed in the public domain.


import liblocation
import gobject


def notify_gps_update(gps_dev):
    # Note: not all structure elements are used here,
    # but they are all made available to python.
    # Accessing the rest is left as an exercise.

    # struct() gives access to the underlying ctypes data.
    # ctypes magically converts things for us.
    gps_struct = gps_dev.struct()
    print 'online', gps_struct.online
    print 'status', gps_struct.status

    # Not sure if fix can ever be None, but check just in case.
    fix = gps_struct.fix
    if fix:
        print 'mode', fix.mode
        print 'gps time', fix.time
        print 'latitude', fix.latitude
        print 'longitude', fix.longitude

    print 'satellites_in_view', gps_struct.satellites_in_view
    print 'satellites_in_use', gps_struct.satellites_in_use

    # satellites is an iterator.
    for sv in gps_struct.satellites:
        print 'prn', sv.prn
        print 'elevation', sv.elevation
        print 'azimuth', sv.azimuth
        print 'signal_strength', sv.signal_strength
        print 'in_use', sv.in_use
    print


def main():

    # required to be initialized when using gpsd_control stuff
    gobject.threads_init()

    # create a gps device object (which is a full pythonic gobject)
    gps = liblocation.gps_device_get_new()

    # connect its gobject 'changed' signal to our callback function
    gps.connect('changed', notify_gps_update)

    # create a gpsd_control object (which is a full pythonic gobject)
    gpsd_control = liblocation.gpsd_control_get_default()

    # are we the first one to grab gpsd?  If so, we can and must
    # start it running.  If we didn't grab it first, then we cannot
    # control it.
    if gpsd_control.struct().can_control:
        liblocation.gpsd_control_start(gpsd_control)   

    # wait for 'changed' event callbacks
    mainloop = gobject.MainLoop()
    mainloop.run()
    

if __name__ == '__main__':
    main()