import gtk
import hildon

class helloWorld(hildon.Program):

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.connect("destroy", gtk.main_quit)
        self.add_window(self.window)
        
        label = gtk.Label("hello Jonas")
        self.window.add(label)
        label.show()
        
        button = gtk.Button("Widget")
        self.window.add(button)
        button.connect("clicked",self.whoop(label))
        button.show()

    def whoop(self):
        self.set_label("tryckt")

    def run(self):
        self.window.show_all()
        gtk.main()
        
app = helloWorld()
app.run()