import gtk
import hildon
import time
import gpsbt

class helloWorld(hildon.Program):

    def gps(self):
        context = gpsbt.start()
        
        if context == None:
            print 'Problem while connecting!'
            return
        
        # ensure that GPS device is ready to connect and to receive commands
        time.sleep(2)
        gpsdevice = gpsbt.gps()
        
        # read 3 times and show information
        for a in range(4):
            gpsdevice.get_fix()
            time.sleep(2)
            
            # print information stored under 'fix' variable
            print 'Altitude: %.3f'%gpsdevice.fix.altitude
            # dump all information available
            print gpsdevice
        
        #Spara GPS coordinater
        alt = gpsdevice.fix.altitude
        long = gpsdevice.fix.longitude
        # ends Bluetooth connection
        gpsbt.stop(context)
        return (alt, long)

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.connect("destroy", gtk.main_quit)
        self.add_wi130ndow(self.window)
        
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
        alt, long = self.gps()
        self.label.set_label(alt + "  "  + long)

    def run(self):
        self.window.show_all()
        gtk.main()
        
app = helloWorld()
app.run()