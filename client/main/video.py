#!/usr/bin/python2.5
# -*- coding: utf-8 -*

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
class GTK_Main:
    def __init__(self):
        print "inne i init"
        #Lite variabler
        #self.ip = '192.168.1.38'
        self.port = '7331'
        self.choice = ''

#        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#        window.set_title("Raddningspatrullen communication system")
#        window.set_default_size(500, 400)
#        window.connect("destroy", gtk.main_quit, "WM destroy")
#        vbox = gtk.VBox()
#        window.add(vbox)
#        self.movie_window = gtk.DrawingArea()
#        vbox.add(self.movie_window)
#        hbox = gtk.HBox()
#        vbox.pack_start(hbox, False)
#        hbox.set_border_width(10)
#        hbox.pack_start(gtk.Label())
#        self.btnAudio = gtk.Button("Voice")
#        self.btnAudio.connect("clicked", self.voice)
#        hbox.pack_start(self.btnAudio, False)
#        self.button2 = gtk.Button("Quit")
#        self.button2.connect("clicked", self.exit)
#        hbox.pack_start(self.button2, False)
#        self.btnVideo = gtk.Button("Video")
#        self.btnVideo.connect("clicked", self.video)
#        hbox.pack_start(self.btnVideo, False)
#        hbox.add(gtk.Label())
#        window.show_all()

    def Stream(self, choice, ip, port):
        print "inne i Stream"
        self.choice = choice
        self.ip = ip
        self.port = port

        if(choice=="Video"):
            print "inne i Stream Video"
            options = "v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host="+ self.ip +" port="+ self.port

            self.player = gst.parse_launch ( options )
            options2 = "udpsrc port="+ self.port +" caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink"
            self.player2 = gst.parse_launch( options2 )

            bus = self.player.get_bus()
            bus.add_signal_watch()
            bus.enable_sync_message_emission()
            bus.connect("message", self.on_message)
            bus.connect("sync-message::element", self.on_sync_message)
            bus2 = self.player2.get_bus()
            bus2.add_signal_watch()
            bus2.enable_sync_message_emission()
            bus2.connect("message", self.on_message)
            bus2.connect("sync-message::element", self.on_sync_message)

        elif(choice=="Voice"):
            options3 = "udpsrc port="+self.port+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink"

            self.player3 = gst.parse_launch ( options3 )
            options4 = "dspilbcsrc dtx=0 ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! udpsink host="+self.ip+" port= "+self.port+""
            self.player4 = gst.parse_launch( options4 )

            bus3 = self.player3.get_bus()
            bus3.add_signal_watch()
            bus3.enable_sync_message_emission()
            bus3.connect("message", self.on_message)
            bus3.connect("sync-message::element", self.on_sync_message)
            bus4 = self.player4.get_bus()
            bus4.add_signal_watch()
            bus4.enable_sync_message_emission()
            bus4.connect("message", self.on_message)
            bus4.connect("sync-message::element", self.on_sync_message)

    #Rostsamtal
    def voice(self, w, ip):
        if ip == None:
            ip = "130.236.219.140"
        print "Voice choosen"
        if(self.btnAudio.get_label() == "Voice"):
            self.btnAudio.set_label("Stop Voice")
            self.choice = "Voice"
            self.Stream(self.choice, ip, self.port)
            self.player3.set_state(gst.STATE_PLAYING)
            self.player4.set_state(gst.STATE_PLAYING)
            #Stream(self.choice, self.ip, self.port)
        else:
            self.choice = ""
            self.player3.set_state(gst.STATE_NULL)
            self.player4.set_state(gst.STATE_NULL)
            self.btnAudio.set_label("Voice")

    #Videosamtal
    def video(self, w, ip):
        if ip == None:
            ip = "130.236.219.140"
        print "Video choosen"
        if self.btnVideo.get_label() == "Video":
            self.btnVideo.set_label("Stop Video")
            self.choice = "Video"
            self.Stream(self.choice, ip, self.port)
            self.player.set_state(gst.STATE_PLAYING)
            self.player2.set_state(gst.STATE_PLAYING)
            #Stream(self.choice, self.ip, self.port)
        else:
            self.choice = ""
            self.player.set_state(gst.STATE_NULL)
            self.player2.set_state(gst.STATE_NULL)
            self.btnVideo.set_label("Video")

    def exit(self, widget, data=None):
        gtk.main_quit()
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            if(self.choice==Video):
                self.player.set_state(gst.STATE_NULL)
                self.player2.set_state(gst.STATE_NULL)
                self.button.set_label("Video")
            elif(self.choice==Voice):
                self.player3.set_state(gst.STATE_NULL)
                self.player4.set_state(gst.STATE_NULL)
                self.button.set_label("Voice")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            if(self.choice==Video):
                self.player.set_state(gst.STATE_NULL)
                self.player2.set_state(gst.STATE_NULL)
                self.btnVideo.set_label("Video")
            elif(self.choice==Voice):
                self.player3.set_state(gst.STATE_NULL)
                self.player4.set_state(gst.STATE_NULL)
                self.btnVoice.set_label("Voice")
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self.movie_window.window.xid)

if __name__ == "__main__":
    GTK_Main()
    gtk.gdk.threads_init()
    gtk.main()
