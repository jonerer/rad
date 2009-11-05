# -*- coding: utf-8 -*
import gpsbt
import time
from shared import rpc
 
def main():
    context = gpsbt.start()
    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    gpsdevice = gpsbt.gps()
    
    # read 3 times and show information
    for a in range(4):
        gpsdevice.get_fix()
        time.sleep(2)
    while gpsdevice.get_position() == (0,0):
        time.sleep(1)  
    x, y = gpsdevice.get_position()
    #stop gps devices
    gpsbt.stop(context)
    return x, y

rpc.set_name("rpcsender")
while True:
    lat, lon = main()
    print rpc.send("main", "ping_with_coordinates", lon=lon, lat=lat)

