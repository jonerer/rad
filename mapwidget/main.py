import gtk
from mapwidget import MapWidget

class MainWindow(gtk.Window):
    mapwidget = None

    def __init__(self):
        gtk.Window.__init__(self)
        self.connect('destroy', gtk.main_quit)

        self.mapwidget = MapWidget(69.3, 15.0)
        self.add(self.mapwidget)

        self.show_all()


if __name__ == '__main__':
    win = MainWindow()
    gtk.main()
