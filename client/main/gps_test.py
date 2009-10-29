import time, gpsbt

def has_a_fix(gps):
    gps.get_fix()
    return gps.satellites_used > 0

con = gpsbt.start()
time.sleep(2.0) # wait for gps to come up
gps = gpsbt.gps()

print "Waiting for the sun... err... a fix"
while not has_a_fix(gps):
    print "Wai-ting..."
    time.sleep(5)

# do something
gpsbt.stop(con)