# -*- coding: utf-8 -*
import gpsbt
import time
from shared import rpc
 
def main():
    rpc.set_name("rpcsender")
    context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    gpsdevice = gpsbt.gps()
    while True:
        #read 3 times and show information
        for a in range(4):
            gpsdevice.get_fix()
            time.sleep(15)
        while gpsdevice.get_position() == (0,0):
            time.sleep(1)  
        lon, lat = gpsdevice.get_position()
        print lon
        print lat
        time.sleep(5)
        print "Nu skickar jag koordinater"
        rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)
        print "skickat koord, updaterar map"
        rpc.send("main", "update_map")
    #stop gps devices
    gpsbt.stop(context)

main()


