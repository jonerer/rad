import gtk
import hildon
import gpsbt
import time

class helloWorld(hildon.Program):
    
    def has_a_fix(self, gps):
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
    #gpsbt.stop(con)
    
    def __init__(self):
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
        
        x = self.gps.longitude
        y = self.gps.latitude
        self.label.set_label(str(x) +"  "+ str(y))
        
        

    def run(self):
        self.window.show_all()
        gtk.main()

        
app = helloWorld()
app.run()