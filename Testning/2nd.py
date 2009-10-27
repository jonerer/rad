import gtk
import hildon

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
        self.button.connect("clicked",self.whoop)
        self.box1.pack_start(self.button, True, True, 0)
        self.box1.pack_start(self.label, True, True, 0)
        self.button.show()
        self.label.show()
        


    def whoop(self, label):
        self.label.set_label("tryckt")

    def run(self):
        self.window.show_all()
        gtk.main()
        
app = helloWorld()
app.run()