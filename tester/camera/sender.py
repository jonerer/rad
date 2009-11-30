import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
class GTK_Main:
	def __init__(self):

		#Lite variabler
                self.ip = '130.236.218.217'
                self.port = '7331'

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                window.set_title("Raddningspatrullen communication system")
                window.set_default_size(500, 400)
                window.connect("destroy", gtk.main_quit, "WM destroy")
                vbox = gtk.VBox()
                window.add(vbox)
                self.movie_window = gtk.DrawingArea()
                vbox.add(self.movie_window)
                hbox = gtk.HBox()

		vbox.pack_start(hbox, False)
                hbox.set_border_width(10)
                hbox.pack_start(gtk.Label())
                self.btnAudio = gtk.Button("Voice")
                self.btnAudio.connect("clicked", self.voice)
                hbox.pack_start(self.btnAudio, False)
                self.button2 = gtk.Button("Quit")
                self.button2.connect("clicked", self.exit)
                hbox.pack_start(self.button2, False)
                self.btnVideo = gtk.Button("Video")
                self.btnVideo.connect("clicked", self.video)
                hbox.pack_start(self.btnVideo, False)
                hbox.add(gtk.Label())
                window.show_all()

	def startVideoOrVoiceConversation(self, choice, ip, port):
		print "inne i startVideoOrVoiceConversation"
		if(self.choice == voice):
			null
		elif(self.choice == video):
			print "inne i choice video"
			#Skickar
			options = "v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host="+ self.ip +" port="+ self.port +""
			self.player = gst.parse_launch ( options )
			#visar
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

	#Rostsamtal
        def voice(self, w):
                print "Voice choosen"
                if(self.btnAudio.get_label() == "Voice"):
                        self.btnAudio.set_label("Stop Voice")
                else:
                        self.btnAudio.set_label("Voice")

        #Videosamtal
        def video(self, w):
                print "Video choosen"
                if self.btnVideo.get_label() == "Video":
                        self.btnVideo.set_label("Stop Video")
                        self.player.set_state(gst.STATE_PLAYING)
                        self.player2.set_state(gst.STATE_PLAYING)
                else:
                        self.player.set_state(gst.STATE_NULL)
                        self.player2.set_state(gst.STATE_NULL)
                        self.btnVideo.set_label("Video")

	def start_stop(self, w):
		if self.button.get_label() == "Start":
			self.button.set_label("Stop")
			self.player.set_state(gst.STATE_PLAYING)
			self.player2.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			self.player2.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
	def exit(self, widget, data=None):
		gtk.main_quit()
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.player2.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)
			self.player2.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)
def main():
	gtk.main()

if __name__ == "__main__":
	MainStream().startVideoOrVoiceConversation(video, 130.236.219.235, 7331)
	gtk.gdk.threads_init()
	gtk.main()
