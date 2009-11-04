#!/usr/bin/python2.5
import rpc

rpc.set_name("lolboll")
print rpc.send("pinger", "ping")
print rpc.send("pinger", "ping_with_id", id=205)
