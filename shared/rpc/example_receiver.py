#!/usr/bin/python2.5
#coding: utf-8

import rpc,gtk
def silent():
    pass

def ping():
    return "pong!"

def ping2(id):
    return "pong me id %d" % id, "eller?"

rpc.set_name("pinger")
rpc.register("ping", ping)
rpc.register("ping_with_id", ping2)
rpc.register("silent", silent)

gtk.main()
