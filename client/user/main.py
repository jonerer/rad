# -*- coding: utf-8 -*
#import gpsbt
import time
from shared import rpc
from shared.data import get_session, create_tables
from shared.data.defs import *

def main():
    rpc.set_name("rpcsender")
   
    #context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    #gpsdevice = gpsbt.gps()

    firstplace = True
    
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
        if firstplace:
            print "Du är inne i firstplace"
            lon = 15.5666574
            lat = 58.39585456
            firstplace = False
        elif not firstplace:
            lon=15.5812375
            lat=58.39972796 
            firstplace = True
        time.sleep(5)
        session = get_session()
        print "innan session"
        for units in session.query(Unit).filter(Unit.is_self==True):
            print "yesh"
            rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)
            print "skickat koord, updaterar map"
            rpc.send("main", "update_map")
    #stop gps devices
    #gpsbt.stop(context)

main()


