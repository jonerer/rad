import gtk
import hildon
import liblocation
import gobject

class helloWorld(hildon.Program):

    def gps(self):
        # required to be initialized when using gpsd_control stuff
        gobject.threads_init()
    
        # create a gps device object (which is a full pythonic gobject)
        gps = liblocation.gps_device_get_new()
    
        # connect its gobject 'changed' signal to our callback function
        gps.connect('changed', self.notify_gps_update)
    
        # create a gpsd_control object (which is a full pythonic gobject)
        gpsd_control = liblocation.gpsd_control_get_default()
    
        # are we the first one to grab gpsd?  If so, we can and must
        # start it running.  If we didn't grab it first, then we cannot
        # control it.
        if gpsd_control.struct().can_control:
            liblocation.gpsd_control_start(gpsd_control)   
    
        # wait for 'changed' event callbacks
        mainloop = gobject.MainLoop()
        try:
            mainloop.run()
        except KeyboardInterrupt:
            print "k."
        
    def notify_gps_update(self, gps_dev):
        # Note: not all structure elements are used here,
        # but they are all made available to python.
        # Accessing the rest is left as an exercise.
    
        # struct() gives access to the underlying ctypes data.
        # ctypes magically converts things for us.
        gps_struct = gps_dev.struct()
        print 'online', gps_struct.online
        print 'status', gps_struct.status
    
        # Not sure if fix can ever be None, but check just in case.
        fix = gps_struct.fix
        if fix:
            print 'mode', fix.mode
            print 'gps time', fix.time
            print 'latitude', fix.latitude
            print 'longitude', fix.longitude
    
        print 'satellites_in_view', gps_struct.satellites_in_view
        print 'satellites_in_use', gps_struct.satellites_in_use
    
        # satellites is an iterator.
        for sv in gps_struct.satellites:
            print 'prn', sv.prn
            print 'elevation', sv.elevation
            print 'azimuth', sv.azimuth
            print 'signal_strength', sv.signal_strength
            print 'in_use', sv.in_use
        print
        self.latitude = fix.latitude
        self.longitude = fix.longitude

    def __init__(self):
        self.gps()
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.connect("destroy", gtk.main_quit)
        self.add_window(self.window)
        
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)
        
        self.label = gtk.Label("hello Jonas")
        self.button = gtk.Button("Widget")
        self.button.connect("clicked",self.whoop)
        self.box1.pack_start(self.button, True, True, 0)
        self.box1.pack_start(self.label, True, True, 0)
        self.button.show()
        self.label.show()
        


    def whoop(self, label):
        self.label.set_label(self.latitude + "  "  + self.longitude)

    def run(self):
        self.window.show_all()
        gtk.main()
        
app = helloWorld()
app.run()