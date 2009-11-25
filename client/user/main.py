# -*- coding: utf-8 -*
import gpsbt
import time
from shared import rpc
from shared.data import get_session, create_tables
from shared.data.defs import *
 
def main():
    rpc.set_name("rpcsender")
    context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    gpsdevice = gpsbt.gps()
    while True:
        # read 3 times and show information
        for a in range(4):
            gpsdevice.get_fix()
            time.sleep(15)
        while gpsdevice.get_position() == (0,0):
            time.sleep(1)  
        lon, lat = gpsdevice.get_position()
        print lon
        print lat
        session = get_session()
        for unit in session.query(Unit).filter(Unit.is_self==True):
            unit.coordx=lon
            unit.coordy=lat
        print unit.coordx
        print unit.coordy
        print "Nu skickar jag koordinater"
        print rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)
        print "skickat koord, updaterar map"
        print rpc.send("main", "update_map")
    #stop gps devices
    gpsbt.stop(context)

main()


