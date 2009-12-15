# -*- coding: utf-8 -*
#import gpsbt
import time
from shared import rpc
from shared.data import get_session, create_tables
from shared.data.defs import *
import gobject
import math

def main():
    rpc.set_name("rpcsender")
   
    #context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    #gpsdevice = gpsbt.gps()

    start_lon = 15.5775752
    start_lat = 58.4065800
    rad = 0.003
    angle_step = 0.1
    angle = 0
    rad2 = 0.005
    angle_step2 = 0.04
    angle2 = 0
    
    while True:
        '''
        #read 3 times and show information
        for a in range(4):
            gpsdevice.get_fix()
            time.sleep(15)
        while gpsdevice.get_position() == (0,0):
            time.sleep(1)  
        lat,lon = gpsdevice.get_position()
        print lon
        print lat
        '''
        lon = start_lon + rad*math.sin(angle)
        lon = lon + rad2*math.sin(angle2)
        print "lon:",lon
        lat = start_lat + rad*math.cos(angle)
        lat = lat + rad2*math.cos(angle2)
        print "lat:",lat
        angle = angle + angle_step
        if angle > 2*math.pi:
            angle - 2*math.pi
        angle2 = angle2 + angle_step2
        if angle2 > 2*math.pi:
            angle2 - 2*math.pi
        time.sleep(1)
        session = get_session()
        for units in session.query(Unit).filter(Unit.is_self==True):
            print "Skickar koordinater", time.time()
            rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)
            #gobject.timeout_add(0, rpc.send, "main", "ping_with_coordinates", {"lon":lon, "lat":lat})

            print "Klar med skickar koordinater", time.time()
    #stop gps devices
    #gpsbt.stop(context)

main()


