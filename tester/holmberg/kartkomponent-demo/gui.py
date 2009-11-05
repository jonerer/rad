# -*- coding: utf-8 -*-
import gtk
import hildon
import gobject
import gui_map
import data_storage
import map_xml_reader


class Gui(hildon.Program):
    _map = None
    _map_change_zoom = None
    
    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False

    def on_key_press(self, widget, event, *args):
        # Ifall "fullscreen"-knappen pￃﾥ handdatorn har aktiverats.
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Pil vￃﾤnster, byter vy
        elif event.keyval == 65361:
            if (self.view.get_current_page() != 0):
                self.view.prev_page()
        # Pil hￃﾶger, byter vy
        elif event.keyval == 65363:
            if (self.view.get_current_page() != 1):
                self.view.next_page()
        # Zoom -
        elif event.keyval == 65477:
            self._map_change_zoom("-")
        # Zoom +
        elif event.keyval == 65476:
            self._map_change_zoom("+")

    def __init__(self, map):
    

        # Initierar hildon (GUI-biblioteket fￃﾶr N810)
        hildon.Program.__init__(self)

        # Sparar handdatorns karta.
        self._map = map
        
        # Skapar programmets fￃﾶnster
        self.window = hildon.Window()
        
        # Nￃﾥgon storlek sￃﾥ att PyGTK inte klagar
        self.window.set_size_request(200, 200)
        # Funktion som kￃﾶrs nￃﾤr prorammet ska stￃﾤngas av
        self.window.connect("destroy", self.menu_exit)
        self.add_window(self.window)

        # Mￃﾶjliggￃﾶr fullscreen-lￃﾤge
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)
        # Programmet ￃﾤr inte i fullscreen-lￃﾤge frￃﾥn bￃﾶrjan.
        self.window_in_fullscreen = False

        # Skapar en notebook-komponent i vilken vi har olika sidor som fungerar
        # som vyer. En sida ￃﾤr fￃﾶr kartvyn, en sida fￃﾶr uppdragsvyn osv.
        # Mer om hur Notebook fungerar stￃﾥr hￃﾤr:
        # http://www.pygtk.org/pygtk2tutorial/sec-Notebooks.html
        self.view = gtk.Notebook()
        self.view.set_show_tabs(False)
        self.view.set_show_border(False)
        self.view.insert_page(self.create_map_view_full())
        self.view.insert_page(self.create_map_view_slice())        
        self.view.insert_page(self.create_settings_view())
        self.view.insert_page(self.create_mission_view())
        
        # Lￃﾤgger in vyn i fￃﾶnstret
        self.window.add(self.view)
        
        # Skapar menyn
        self.window.set_menu(self.create_menu())

    def create_mission_view(self):
        frame = gtk.Frame("Uppdrag")
        frame.set_border_width(5)
        label = gtk.Label("ANALYZING DATA...afa")
        #frame.add(label)
        
        label2 = gtk.Label("poop")
        label2.show()
        entry = gtk.Entry()
        entry.set_max_length(100)
        #entry.connect("activate", self.enter_callback, entry)
        entry.set_text("")
        entry.select_region(0, len(entry.get_text()))
        entry.show()
        frame.add(entry)
        
        return frame
        
    
    # Skapar vyn fￃﾶr kartan
    def create_map_view_slice(self):
       # frame = gtk.Frame(self._map.name + " <longitude, latitude>")
        map = gui_map.Map(self._map)
        arrowButton = gtk.Button();
        arrow = gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_OUT);
        arrowButton.add(arrow)
        arrowButton.show()
        arrow.show()
        
        frame2 = gtk.Frame("Status")
        frame2.set_border_width(2)
        box = gtk.HBox(False, 0)
        box.pack_start(map, expand=True, fill=True, padding=0)
        box.pack_start(arrowButton, expand=False, fill=False, padding=0)


        frame2.show()
        box.show()

        # Sparar undan funktionen som mￃﾶjliggￃﾶr zoomning
        self._map_change_zoom = map.change_zoom
        return box
        
    def create_map_view_full(self):
        frame = gtk.Frame(self._map.name + " <longitude, latitude>")
        frame.set_border_width(5)
        map = gui_map.Map(self._map)
        frame.add(map)
        
        # Sparar undan funktionen som mￃﾶjliggￃﾶr zoomning
        self._map_change_zoom = map.change_zoom
        return frame
        
    # Skapar vyn fￃﾶr instￃﾤllningar
    def create_settings_view(self):
        frame = gtk.Frame("Instￃﾤllningar")
        frame.set_border_width(5)

        # Skicka GPS-koordinater till basen?
        hbox2 = gtk.HBox(homogeneous=False, spacing=0)
        lblSkickaGPSKoordinater = gtk.Label("Skicka GPS koordinater till basen")
        lblSkickaGPSKoordinater.set_justify(gtk.JUSTIFY_LEFT)
        chkSkickaGPSKoordinater = gtk.CheckButton("Ja")
        #chkSkickaGPSKoordinater.connect("toggled", self.chkSkickaGPSKoordinater_callback)
        hbox2.pack_start(lblSkickaGPSKoordinater, True, True, 5)
        hbox2.pack_start(chkSkickaGPSKoordinater, False, False, 5)

        # Skapar knappen som sparar instￃﾤllningarna
        btnSpara = gtk.Button("Spara!")
        btnSpara.connect("clicked", self.handle_menu_items, 0)

        vbox = gtk.VBox(homogeneous=False, spacing=0)
        #vbox.pack_start(hbox1, False, False, 0)
        vbox.pack_start(hbox2, False, False, 5)
        vbox.pack_start(btnSpara, False, False, 5)

        frame.add(vbox)
        return frame

    # Skapar en meny som kommer ligga lￃﾤngst upp i vￃﾥrt program.
    def create_menu(self):
        # Skapar tre stycken meny-inlￃﾤgg.
        menuItemKartaFull = gtk.MenuItem("Karta - Full")
        menuItemKartaSlice = gtk.MenuItem("Karta - Delad")
        menuItemSeparator = gtk.SeparatorMenuItem()
        menuItemUppdrag = gtk.MenuItem("Tuffa Uppdrag")
        menuItemInstallningar = gtk.MenuItem("Instￃﾤllningar")
        menuItemSeparator = gtk.SeparatorMenuItem()
        menuItemExit = gtk.MenuItem("Exit")

        menuItemKartaFull.connect("activate", self.handle_menu_items, 0)
        menuItemKartaSlice.connect("activate", self.handle_menu_items, 1)
        menuItemInstallningar.connect("activate", self.handle_menu_items, 2)
        menuItemUppdrag.connect("activate", self.handle_menu_items, 3)
        menuItemExit.connect("activate", self.menu_exit)

        # Skapar en meny som vi lￃﾤgger in dessa inlￃﾤgg i.
        menu = gtk.Menu()
        menu.append(menuItemKartaFull)
        menu.append(menuItemKartaSlice)
        menu.append(menuItemSeparator)
        menu.append(menuItemInstallningar)
        menu.append(menuItemUppdrag)
        menu.append(menuItemSeparator)
        menu.append(menuItemExit)

        return menu

    def get_treeview(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args[2]

    def get_row_number_from_treeview(self, treeview):
        row = treeview.get_selection().get_selected_rows()
        return row[1][0][0]

    # Denna funktion har skapats eftersom det ￃﾤr aningen omstￃﾤndigt att fￃﾥ ut
    # vￃﾤrden frￃﾥn en markering i en lista. Skicka in listan och kolumnen du
    # vill ha ut vￃﾤrdet ifrￃﾥn sￃﾥ skￃﾶter funktionen resten. Fￃﾶrsta kolumnen ￃﾤr 0,
    # andra 1 osv. 
    def get_value_from_treeview(self, treeview, column):
        # Lￃﾤs mer om vad row innehￃﾥller hￃﾤr (gtk.TreeSelection.get_selected_row):
        # http://www.pygtk.org/pygtk2reference/class-gtktreeselection.html
        row = treeview.get_selection().get_selected_rows()
      
        if len(row[1]) > 0:
            # row innehￃﾥller en tuple med (ListStore(s), path(s))
            # Vi plockar ut fￃﾶrsta vￃﾤrdet i paths. Eftersom vi enbart tillￃﾥter
            # anvￃﾤndaren att markera en rad i taget kommer det alltid bara finnas
            # ett vￃﾤrde i paths.
            path = row[1][0]
          
            # Hￃﾤmtar modellen fￃﾶr treeview
            treemodel = treeview.get_model()
          
            # Returnerar vￃﾤrdet
            return treemodel.get_value(treemodel.get_iter(path), column)
        else:
            return None

    def handle_menu_items(self, widget, num):
        self.view.set_current_page(num)

    def menu_exit(self, widget, data=None):
        # Stￃﾤnger net GUI:t.
        gtk.main_quit()

    def run(self):
        self.window.show_all()
        gtk.main()
