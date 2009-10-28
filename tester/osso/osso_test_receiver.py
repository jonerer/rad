#!/usr/bin/python2.5
import osso, gtk
def callback_func(interface, method, arguments, user_data):
    print "RPC received"

    osso_c = user_data
    osso_c.system_note_infoprint("osso_test_receiver: Received a RPC to %s." % method)
    osso_c = oso.Context("osso_test_receiver", "0.0.1", False)
print "osso_test_receiver started" 
osso_c.set_rpc_callback("spam.eggs.osso_test_receiver", 
        "/spam/eggs/osso-test_receiver", 
        "spam.eggs.osso_test_receiver", callback_func, osso_c)
gtk.main()


