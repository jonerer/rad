# -*- coding: utf-8 -*-
import gtk
import hildon
import gui_map
import time
from shared.data import get_session, create_tables
from shared.data.defs import *
from shared import rpc, packet

def create_menuButton(bild,label):
    buttonBox = gtk.HBox(False, spacing=1)
    button = gtk.Button()
    label = gtk.Label(label)
    buff = gtk.gdk.PixbufAnimation(bild)
    image = gtk.Image()
    image.set_from_animation(buff)
    image.show()
    label.show()
    buttonBox.pack_start(image, expand=False, fill=False, padding=5)
    buttonBox.pack_start(label, expand=False, fill=False, padding=5)
    button.add(buttonBox)
    button.show_all()
    button.set_size_request(100, 60)
    return button

class Page(gtk.VBox):
    def __init__(self, name, gui, width="half", spacing=1, homogeneous=False):
        super(gtk.VBox, self).__init__(homogeneous=homogeneous, spacing=spacing)
        if width == "half":
            self.size_request = (300,300)
        elif width == "full":
            self.size_request = (600,300)
        self.show()
        self.gui = gui

    def map_dblclick(self, coordx, coordy):
        pass
        #print "got dblclick i Page! coords: %s, %s" % (coordx,coordy)

class MenuPage(Page):
    def mission_button_clicked(self, widget, data=None):
        self.gui.switch_page("mission")

    def hille_e_tjock(self, widget, data=None):
        print "tjockade på hille"
        poi = str(packet.Packet("poi",id = "", sub_type = "skogsbrand", name = "Vallarondellen", timestamp = time.time(), coordx = "15.57796", coordy = "58.40479"))
        rpc.send("qos", "add_packet", packet=poi)
        #alarm = str(packet.Packet("alarm", id = "", sub_type = "skogsbrand", name = "Vallarondellen", timestamp = time.time(), poi_id = "", contact_person = "", contact_number = "", other = ""))
        #print rpc.send("qos", "add_packet", packet=alarm)


    def __init__(self, gui):
        super(MenuPage, self).__init__("menu", gui)
        
        # CREATE BUTTONS
        mapButton = create_menuButton("static/ikoner/map.png","Karta")
        setButton = create_menuButton("static/ikoner/cog.png","Installningar")
        conButton = create_menuButton("static/ikoner/book_addresses.png","Kontakter")
        misButton = create_menuButton("static/ikoner/book.png","Uppdrag")
        jonasButton = create_menuButton("static/ikoner/JonasInGlases.png","Jonas")
        misButton.connect("clicked", self.mission_button_clicked, None)
        setButton.connect("clicked", self.gui.switch_page, "settings")
        conButton.connect("clicked", self.hille_e_tjock, None)
      
        # MISSION ADD
        vMissionAddBox = gtk.VBox(False,0)
        unitNameLabel = gtk.Label("Namn på objekt:")
        unitTypeLabel = gtk.Label("Typ av objekt:")
        unitName = gtk.Entry()
        typeBox = gtk.Combo()
        typeBox.set_size_request(100,100)
        slist = [ "Brandbil", "Ambulans", "Schnase", "Jonas" ]
        typeBox.set_popdown_strings(slist)

        vMissionAddBox.pack_start(unitNameLabel, False,True,2)
        vMissionAddBox.pack_start(unitName,False,True,2)
        vMissionAddBox.pack_start(unitTypeLabel, False,True,2)
        vMissionAddBox.pack_start(typeBox,False,True,2)
        self.pack_start(vMissionAddBox,False,True,2)
      
        vMissionAddBox.show_all()
        vMissionAddBox.hide()

        vMenuBox = gtk.VBox(False,0)
        vMenuBox.pack_start(mapButton, False, True, padding=2)
        vMenuBox.pack_start(misButton, False, True, padding=2)
        vMenuBox.pack_start(conButton, False, True, padding=2)
        vMenuBox.pack_start(setButton, False, True, padding=2)
        vMenuBox.pack_start(jonasButton, False, True, padding=2)
        self.pack_start(vMenuBox, False, False, padding=2)
        
        self.show()
        vMenuBox.show()

class SettingsPage(Page):
    def __init__(self, gui):
        super(SettingsPage, self).__init__("settings", gui, width="full")

        button = create_menuButton("static/ikoner/arrow_left.png", "Tillbaka")
        button.connect("clicked", self.gui.switch_page, "menu")
        self.pack_start(button, False, False, padding=2)

        self.show_all()
        
class MissionPage(Page):

    def __init__(self, gui):
        super(MissionPage, self).__init__("mission", gui, homogeneous=False,
                spacing=0)
        newMissionButton = create_menuButton("static/ikoner/book_add.png",
                "Lagg till")
        editMissionButton = create_menuButton("static/ikoner/book_edit.png",
                "Redigera")
        deleteMissionButton = create_menuButton("static/ikoner/book_delete.png",                     "Ta bort")
        backButton = create_menuButton("static/ikoner/arrow_left.png","Tillbaka")
        
        backButton.connect("clicked", self.gui.switch_page, "menu")
        newMissionButton.connect("clicked", self.gui.switch_page, "addMission")
        self.pack_start(newMissionButton, False, False, padding=2)
        self.pack_start(editMissionButton, False, False, padding=2)
        self.pack_start(deleteMissionButton, False, False, padding=2)
        self.pack_start(backButton, False, False, padding=2)

        self.show_all()

class AddMissionPage(Page):

    def __init__(self, gui):
        super(AddMissionPage, self).__init__("addMission", gui, homogeneous=False,
                spacing=0)
        
        def dbupdate_press_callback(self, widget, data=None):   
            name = unicode(nameEntry.get_text())
            info = unicode(infoEntry.get_text())
            xEntry = unicode(xEntry.get_text())
            yEntry = unicode(yEntry.get_text())
            mission_save = str(packet.Packet("mission_save", name=name,\
                                info=info, xEntry=xEntry, yEntry=yEntry))
            print rpc.send("qos", "mission_save", packet=mission_save)
        
        nameLabel = gtk.Label("Namn:")
        nameEntry = gtk.Entry()
        infoLabel = gtk.Label("Info:")
        infoEntry = gtk.Entry()
        xLabel = gtk.Label("X-koordinat:")
        xEntry = gtk.Entry()
        yLabel = gtk.Label("Y-koordinat:")
        yEntry = gtk.Entry()
        #infoView = gtk.TextView(None)
        #infoView.set_editable(True)
        #infoTextBuffer = infoView.get_buffer()
        #infoScroll = gtk.ScrolledWindow()
        #infoScroll.set_size_request(294,150)
        #infoScroll.add(infoView)
        #infoScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        #infoView.set_wrap_mode(gtk.WRAP_WORD)
        
        self.pack_start(nameLabel, False, False,0)
        self.pack_start(nameEntry, False, False,0)
        self.pack_start(infoLabel, False, False,0)
        self.pack_start(infoEntry, False, False,0)
        self.pack_start(xLabel, False, False,0)
        self.pack_start(xEntry, False, False,0)
        self.pack_start(yLabel, False, False,0)
        self.pack_start(yEntry, False, False,0)
        
        saveButton = create_menuButton("static/ikoner/disk.png","Spara")
        backButton = create_menuButton("static/ikoner/arrow_undo.png","Avbryt")
        backButton.connect("clicked", self.gui.switch_page, "mission")
        okButton.connect("clicked", dbupdate_press_callback, None)
        
        hbox1 = gtk.HBox()
        hbox1.pack_start(backButton, True, True, padding=2)
        hbox1.pack_start(saveButton, True, True, padding=2)
        self.pack_start(hbox1, False, False, 2)
        

        self.show_all()

class Gui(hildon.Program):
    _map = None
    _map_change_zoom = None

    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False

    def on_key_press(self, widget, event, *args):
        # Ifall "fullscreen"-knappen på handdatorn har aktiverats.
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Pil vänster, byter vy
        elif event.keyval == 65361:
            if (self.view.get_current_page() != 0):
                self.view.prev_page()
        # Pil höger, byter vy
        elif event.keyval == 65363:
            if (self.view.get_current_page() != 1):
                self.view.next_page()
        # Zoom -    
        elif event.keyval == 65477:
            self._map_change_zoom("-")
        # Zoom +
        elif event.keyval == 65476:
            self._map_change_zoom("+")
    # __INIT__------------------
    #       Description: the INIT funktion...
    def __init__(self, map):
        # Initierar hildon (GUI-biblioteket för N810)
        hildon.Program.__init__(self)

        # Sparar handdatorns karta.
        self._map = map

        # Skapar programmets fönster
        self.window = hildon.Window()
        # Någon storlek så att PyGTK inte klagar
        self.window.set_size_request(200, 200)
        # Funktion som körs när prorammet ska stängas av
        self.window.connect("destroy", self.menu_exit)
        self.add_window(self.window)

        self._pages = {}
        self._pages["menu"] = MenuPage(self)
        self._pages["mission"] = MissionPage(self)
        self._pages["settings"] = SettingsPage(self)
        self._pages["addMission"] = AddMissionPage(self)


        # Möjliggör fullscreen-läge
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)
        # Programmet är inte i fullscreen-läge från början.
        self.window_in_fullscreen = False

        
        self.view = gtk.Notebook()
        self.view.set_show_tabs(False)
        self.view.set_show_border(False)
        self.view.insert_page(self.create_map_view())
        self.view.insert_page(self.create_settings_view())
        self.view.insert_page(self.create_login_view())
        self.view.show()
        # Lägger in vyn i fönstret
        self.window.add(self.view)

        # Skapar menyn
        self.window.set_menu(self.create_menu())
    # // __INIT__-----------------
    
    def switch_page(self, page_name, widget=None):
        # if widget is supplied, it actually contains page_name, so swap!
        if widget is not None:
            page_name = widget
        num = self.rightBook.page_num(self._pages[page_name])
        self.rightBook.set_size_request(*self._pages[page_name].size_request)
        self.rightBook.set_current_page(num)

    def map_dblclick(self, coordx, coordy):
        active_page = self.rightBook.get_nth_page(self.rightBook.get_current_page())
        active_page.map_dblclick(coordx, coordy)
    
    # QUICK MENU ------------------------
    #       Description: Creates our quickmenu with the basic four buttons
    def create_quickMenu(self):
        menuBox = gtk.HBox()
        no = gtk.Label("No Active Object")
        
        
        mainButton = gtk.Button()
        menuBox.pack_start(mainButton)
        buff1 = gtk.gdk.PixbufAnimation("static/ikoner/cog.png")
        image1 = gtk.Image()
        image1.set_from_animation(buff1)
        image1.show()
        mainButton.add(image1)
        mainButton.connect("clicked", self.handle_menu_items, 3)
        mainButton.set_size_request(70, 70)
        
        
        missionButton = gtk.Button()
        menuBox.pack_start(missionButton)
        buff2 = gtk.gdk.PixbufAnimation("static/ikoner/book_addresses.png")
        image2 = gtk.Image()
        image2.set_from_animation(buff2)
        image2.show()
        missionButton.add(image2)
        missionButton.set_size_request(70, 70)
        
        missionButton2 = gtk.Button()
        menuBox.pack_start(missionButton2)
        buff3 = gtk.gdk.PixbufAnimation("static/ikoner/paste_plain.png")
        image3 = gtk.Image()
        image3.set_from_animation(buff3)
        image3.show()
        missionButton2.add(image3)
        missionButton2.set_size_request(70, 70)
        
        missionButton3 = gtk.Button()
        menuBox.pack_start(missionButton3)
        buff4 = gtk.gdk.PixbufAnimation("static/ikoner/map.png")
        image4 = gtk.Image()
        image4.set_from_animation(buff4)
        image4.show()
        missionButton3.add(image4)
        missionButton3.connect("clicked", self.handle_menu_items, 0)
        missionButton3.set_size_request(70, 70)
        
        menuBox.show()
        mainButton.show()
        missionButton.show()
        missionButton2.show()
        missionButton3.show()
        menuBox.set_spacing(0)

        return menuBox
    # // QUICK MENU ------------------------
    
    #  MAP-View------------ID 0------------------
    #       Description: The mapview :P
    def create_map_view(self):
      
        def openButton_press_callback(button, widget, data=None):
            openButton.hide()
            closeButton.show()
            vbox1.show()
            self.switch_page("menu")
            
        def closeButton_press_callback(button, widget, data=None):
            openButton.show()
            closeButton.hide()
            vbox1.hide()
            return        
        
        def show_mission(self, widget, data=None):
            menuBox.hide()
            return
        
        hbox1 = gtk.HBox(homogeneous=False, spacing=1)
        hbox2 = gtk.HBox(homogeneous=False, spacing=1)
        vbox1 = gtk.VBox(homogeneous=False, spacing=1)
        map = gui_map.Map(self._map, self)
        
        #SHOW / HIDE buttons----------------------
        openButton = gtk.Button()
        buff5 = gtk.gdk.PixbufAnimation("static/ikoner/resultset_first.png")
        openArrow = gtk.Image()
        openArrow.set_from_animation(buff5)
        openArrow.show()
        openButton.connect("clicked", openButton_press_callback, None)
        
        closeButton = gtk.Button()
        buff6 = gtk.gdk.PixbufAnimation("static/ikoner/resultset_last.png")
        closeArrow = gtk.Image()
        closeArrow.set_from_animation(buff6)
        closeArrow.show()
        
        closeButton.connect("clicked", closeButton_press_callback, None) 
        openButton.add(openArrow)
        openButton.show()
        openArrow.show()
        closeButton.add(closeArrow)
        closeButton.hide()
        closeArrow.show()
        
        # MENUBOX-----------------------
        rightBook = gtk.Notebook()
        missionBox = gtk.VBox(False,1)
        for page in self._pages.values():
            rightBook.insert_page(page)
        rightBook.set_show_tabs(False)
        rightBook.set_show_border(False)
        rightBook.show()
        self.rightBook = rightBook
        
        # MISSIONBOX-----------------------

        hbox1.pack_start(map, expand=True, fill=True, padding=0)
        hbox1.pack_start(hbox2, expand=False, fill=False, padding=0)
        hbox2.pack_start(openButton, expand=False, fill=False, padding=0)
        hbox2.pack_start(closeButton, expand=False, fill=False, padding=0)
        hbox2.pack_start(vbox1, False, False, 0)
        
        vbox1.pack_start(rightBook, False, False, padding=0)
        
        hbox1.show()
        hbox2.show()
        map.show()
        # Sparar undan funktionen som möjliggör zoomning
        self._map_change_zoom = map.change_zoom
        
        return hbox1
    #  // MAP-VIEW------------ID 0------------
    
    #  LOGIN-View------------ID 2------------------
    #       Description: Simple loginframe to handle logins, daa!!

    def create_login_view(self):
        def dbcheck_press_callback(self, widget, data=None):   
            #Detta behövs inte här, men kanske inte fungerar på andra stället
            #session = get_session()
            #create_tables()        
            #session.bind
            #session.query(User).all()
            user = unicode(userText.get_text())
            pw = unicode(passText.get_text())
            login = str(packet.Packet("login", username=user, password=pw))
            print rpc.send("qos", "add_packet", packet=login)

        def access(bol):
            if bol:
                statusLabel.set_label("Access granted")
            if not bol:
                statusLabel.set_label("Access denied")

        hboxOUT  = gtk.HBox(homogeneous=False, spacing=1)
        vbox1 = gtk.VBox(homogeneous=False, spacing=1)
        hbox1 = gtk.HBox(homogeneous=False, spacing=1)
        hbox2 = gtk.HBox(homogeneous=False, spacing=1)
        userText = gtk.Entry(max=0)
        userLabel = gtk.Label("Användare")
        passText = gtk.Entry(max=0)
        passLabel = gtk.Label("Lösenord")
        okButton = gtk.Button("Login")
        okButton.set_size_request(70, 50)
        okButton.connect("clicked", dbcheck_press_callback, None)
        statusLabel = gtk.Label("No status")

        vbox1.pack_start(hbox1, expand=False, fill=False, padding=1)
        vbox1.pack_start(hbox2, expand=False, fill=False, padding=1)
        vbox1.pack_start(okButton, expand=False, fill=False, padding=1)
        hbox1.pack_start(userText, expand=False, fill=False, padding=1)
        hbox1.pack_start(userLabel, expand=False, fill=False, padding=1)
        hbox2.pack_start(passText, expand=False, fill=False, padding=1)
        hbox2.pack_start(passLabel, expand=False, fill=False, padding=1)
        vbox1.pack_start(statusLabel, expand=False, fill=False, padding=1)
        hboxOUT.pack_start(vbox1, expand=True, fill=False, padding=1)
        
        userText.show()
        userLabel.show()
        passText.show()
        passLabel.show()
        okButton.show()
        statusLabel.show()
        hbox1.show()
        hbox2.show()
        vbox1.show()
        hboxOUT.show()
        #Skapar rpc
        rpc.register("access", access)
        
        return hboxOUT
    #  // LOGIN-View------------ID 2------------------

    #  SETTINGS-View------------ID 1------------------
    #       Description: Will handle all kind of settings possible
    def create_settings_view(self):
        frame = gtk.Frame("Inställningar")
        frame.set_border_width(5)

        # Skicka GPS-koordinater till basen?
        hbox2 = gtk.HBox(homogeneous=False, spacing=0)
        lblSkickaGPSKoordinater = gtk.Label("Skicka GPS koordinater till basen")
        lblSkickaGPSKoordinater.set_justify(gtk.JUSTIFY_LEFT)
        chkSkickaGPSKoordinater = gtk.CheckButton("Ja")
        #chkSkickaGPSKoordinater.connect("toggled", self.chkSkickaGPSKoordinater_callback)
        hbox2.pack_start(lblSkickaGPSKoordinater, True, True, 5)
        hbox2.pack_start(chkSkickaGPSKoordinater, False, False, 5)

        # Skapar knappen som sparar inställningarna
        btnSpara = gtk.Button("Spara!")
        btnSpara.connect("clicked", self.handle_menu_items, 0)

        vbox = gtk.VBox(homogeneous=False, spacing=0)
        #vbox.pack_start(hbox1, False, False, 0)
        vbox.pack_start(hbox2, False, False, 5)
        vbox.pack_start(btnSpara, False, False, 5)

        frame.add(vbox)
        frame.show_all()
        return frame
    #  // SETTINGS-View------------ID 1------------------

    #  TOP MENU------------------------------
    #       Description: Creates the dropdown-menu, its placed at the top left tab
    def create_menu(self):
        # Skapar tre stycken meny-inlägg.
        menuItemKarta = gtk.MenuItem("Karta")
        menuItemInstallningar = gtk.MenuItem("Inställningar")
        menuItemLogin = gtk.MenuItem("Login")
        menuItemSeparator = gtk.SeparatorMenuItem()
        menuItemExit = gtk.MenuItem("Exit")

        menuItemKarta.connect("activate", self.handle_menu_items, 0)
        menuItemInstallningar.connect("activate", self.handle_menu_items, 1)
        menuItemLogin.connect("activate", self.handle_menu_items, 2)
        menuItemExit.connect("activate", self.menu_exit)

        # Skapar en meny som vi lägger in dessa inlägg i.
        menu = gtk.Menu()
        menu.append(menuItemKarta)
        menu.append(menuItemInstallningar)
        menu.append(menuItemLogin)
        menu.append(menuItemSeparator)
        menu.append(menuItemExit)

        return menu
    #  // TOP MENU------------------------------
    def get_treeview(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args[2]

    def get_row_number_from_treeview(self, treeview):
        row = treeview.get_selection().get_selected_rows()
        return row[1][0][0]

    # Denna funktion har skapats eftersom det är aningen omständigt att få ut
    # värden från en markering i en lista. Skicka in listan och kolumnen du
    # vill ha ut värdet ifrån så sköter funktionen resten. Första kolumnen är 0,
    # andra 1 osv. 
    def get_value_from_treeview(self, treeview, column):
        # Läs mer om vad row innehåller här (gtk.TreeSelection.get_selected_row):
        # http://www.pygtk.org/pygtk2reference/class-gtktreeselection.html
        row = treeview.get_selection().get_selected_rows()
      
        if len(row[1]) > 0:
            # row innehåller en tuple med (ListStore(s), path(s))
            # Vi plockar ut första värdet i paths. Eftersom vi enbart tillåter
            # användaren att markera en rad i taget kommer det alltid bara finnas
            # ett värde i paths.
            path = row[1][0]
          
            # Hämtar modellen för treeview
            treemodel = treeview.get_model()
          
            # Returnerar värdet
            return treemodel.get_value(treemodel.get_iter(path), column)
        else:
            return None

    def handle_menu_items(self, widget, num):
        self.view.set_current_page(num)

    def menu_exit(self, widget, data=None):
        # Stänger net GUI:t.
        gtk.main_quit()

    def run(self):
        self.window.show()
        gtk.main()
