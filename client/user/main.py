# -*- coding: utf-8 -*
import gpsbt
import time
from shared import rpc
 
def main():
    rpc.set_name("rpcsender")
    #context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    #time.sleep(2)
    #gpsdevice = gpsbt.gps()
    while True:
        # read 3 times and show information
        #for a in range(4):
            #gpsdevice.get_fix()
            #time.sleep(15)
        #while gpsdevice.get_position() == (0,0):
            #time.sleep(1)  
        #lon, lat = gpsdevice.get_position()
        time.sleep(5)
        lon = 15.5629
        lat = 58.4093
        print lon
        print lat
        print "Nu skickar jag koordinater"
        print rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)
        print "skickat koord, updaterar map"
        print rpc.send("main", "update_map")
        lon = lon + 00.0010
        lat = lat + 00.0010
    #stop gps devices
    gpsbt.stop(context)

main()


