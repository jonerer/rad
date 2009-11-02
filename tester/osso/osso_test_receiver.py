#!/usr/bin/python2.5
# coding: utf-8
import osso, gtk, thread, random
def callback_func(interface, method, arguments, user_data):
    try:
        print "RPC received: method, args, data %s %s %s" % (method, arguments, user_data)

        osso_c = user_data
    except Exception, e:
        print "jävla bajs lr? :S %s" % e
    return "minibajz"
osso_c = osso.Context("osso_test_receiver", "0.0.1", False)
print osso_c
osso_rpc = osso.Rpc(osso_c)
print osso_rpc
osso_rpc.set_rpc_callback("spam.eggs.osso_test_receiverz", 
        "/spam/eggs/osso-test_receiver", 
        "spam.eggs.osso_test_receiver", callback_func, osso_c)
#thread.start_new_thread(gtk.main, tuple())
gtk.main()
print "hax'd"
# not works lol

