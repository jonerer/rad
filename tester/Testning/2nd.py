import gtk
import hildon
import gps


class helloWorld(hildon.Program):
    
    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.connect("destroy", gtk.main_quit)
        self.add_window(self.window)
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)
        self.label = gtk.Label("hello Jonas")
        
        self.button = gtk.Button("Widget")
        self.button2 = gtk.Button("lek")
        
        self.button.connect("clicked",self.whoop)
        self.button2.connect("clicked",self.whip)
        
        self.box1.pack_start(self.button, True, True, 0)
        self.box1.pack_start(self.label, True, True, 0)
        self.box1.pack_start(self.button2, True, True, 0)
        
        self.button.show()
        self.button2.show()
        self.label.show()
        
    def whip(self, label):
        self.label.set_label("tjenare")
    def whoop(self, label):
        self.label.set_label("whip")
        x, y = gps.main()
        self.label.set_label("Lat: "+ str(x) +"  Lon: "+ str(y))

    def run(self):
        self.window.show_all()
        gtk.main()
    
app = helloWorld()
app.run()