#!/usr/bin/python2.5
import osso, hildon, gtk
def send_rpc(widget, osso_c):
    osso_rpc = osso.Rpc(osso_c)
    rpc_val = osso_rpc.rpc_run("spam.eggs.osso_test_receiverz",
            "/spam/eggs/osso_test_receiver",
            "spam.eggs.osso_test_receiver", "do_something", ("weo","hm"), wait_reply=True)
    print "RPC sent. Val received: %s, %s" % (rpc_val, type(rpc_val))
osso_c = osso.Context("osso_test_sender", "0.0.1", False)
window = hildon.Window()
window.connect("destroy", gtk.main_quit)
send_button = gtk.Button("Send RPC")
window.add(send_button)
send_button.connect("clicked", send_rpc, osso_c)
window.show_all()
gtk.main()
