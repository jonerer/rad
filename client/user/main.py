# -*- coding: utf-8 -*
#import gpsbt
import time
from shared import rpc
from shared.data import get_session, create_tables
from shared.data.defs import *

def main():
    rpc.set_name("rpcsender")
    '''
    context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    gpsdevice = gpsbt.gps()
    '''
    lon,lat = 15.5607839,58.3971288
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
        time.sleep(5)
        lon = lon + 0.002
        lat = lat + 0.002
        session = get_session()
        for units in session.query(Unit).filter_by(is_self=True):
            print "yesh"
            rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)
            print "skickat koord, updaterar map"
            rpc.send("main", "update_map")
    #stop gps devices
    gpsbt.stop(context)

main()


