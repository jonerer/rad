#!/usr/bin/python2.5
import rpc, gtk

def async_cb(val):
    print "async_cb: %s" % (val)

rpc.set_name("lolboll")
print rpc.send("pinger", "ping")
print rpc.send("pinger", "ping_with_id", id=205)
rpc.send_async("pinger", "ping", callback=async_cb)
rpc.send_async("pinger", "silent", callback=async_cb)
rpc.send_async("pinger", "ping_with_id", callback=async_cb, id=302)
rpc.send_async("pinger", "ping_with_id", id=402)

gtk.main()
