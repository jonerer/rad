#!/usr/bin/env python

# example-start buttons buttons.py
import hildon
import pygtk
pygtk.require('2.0')
import gtk

# Create a new hbox with an image and a label packed into it
# and return the box.


class Buttons:
    # Our usual callback method
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Image'd Buttons!")


        self.skriv = gtk.Entry()

        button = gtk.Button()


        self.skriv.show()

        self.window.add(self.skriv)
        self.window.show()

def main():
    gtk.main()
    return 0     

if __name__ == "__main__":
    Buttons()
    main()
