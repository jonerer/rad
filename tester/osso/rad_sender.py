#!/usr/bin/python2.5
import rpc

rpc.set_name("lolboll")
rpc.send("pinger", "ping")
rpc.send("pinger", "ping_with_id", id=205)
