# -*- coding: utf-8 -*
import gtk
import hildon
import gui_map
import time
from shared.data import get_session, create_tables
from shared.data.defs import *
from shared import rpc, packet
from datetime import datetime


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
    def hille_e_tjock(self, widget, data=None):
        print "tjockade på hille"
        session = get_session()
        poiPacket = str(packet.Packet("poi",id = "", sub_type = u"brand", name = "Vallarondellen", coordx = "15.5680", coordy = "58.4100"))
        rpc.send("qos", "add_packet", packet=poiPacket)
        #alarm = str(packet.Packet("alarm", id = "", sub_type = "skogsbrand", name = "Vallarondellen", timestamp = time.time(), poi_id = "", contact_person = "", contact_number = "", other = ""))
        #print rpc.send("qos", "add_packet", packet=alarm)

        
    def add_hille(self, pack):
        pack = packet.Packet.from_str(str(pack))
        session = get_session()
        connection.timestamp = time.time()
        loginfo = pack.data
        id = pack.data["id"]
        name = pack.data["name"]
        timestamp = pack.timestamp
        sub_type = pack.data["sub_type"]
        coordx = pack.data["coordx"]
        coordy = pack.data["coordy"]
        for poi_types in session.query(POIType).filter(POIType.name==sub_type):
            type = poi_types
        print session.add(POI(coordx, coordy, id, name, type, timestamp))
        session.commit()
        for poi in session.query(POI).filter(poi.name == name):
            map.add_object(poi.name, data_storage.MapObject(
                {"longitude":poi.coordx,"latitude":poi.coordy},
                poi.type.image))

    def __init__(self, gui):
        super(MenuPage, self).__init__("menu", gui)
        self.size_request = (300,300)
        # CREATE BUTTONS
        objButton = create_menuButton("static/ikoner/JonasInGlases.png","Objekt")
        setButton = create_menuButton("static/ikoner/cog.png","Installningar")
        conButton = create_menuButton("static/ikoner/book_addresses.png","Kontakter")
        misButton = create_menuButton("static/ikoner/book.png","Uppdrag")
        jonasButton = create_menuButton("static/ikoner/JonasInGlases.png","Jonas")
        objButton.connect("clicked", self.gui.switch_page, "object")
        misButton.connect("clicked", self.gui.switch_page, "mission")
        setButton.connect("clicked", self.gui.switch_page, "settings")
        conButton.connect("clicked", self.gui.switch_page, "contact")
        jonasButton.connect("clicked", self.hille_e_tjock)

        vMenuBox = gtk.VBox(False,0)
        vMenuBox.pack_start(objButton, False, True, padding=2)
        vMenuBox.pack_start(misButton, False, True, padding=2)
        vMenuBox.pack_start(conButton, False, True, padding=2)
        vMenuBox.pack_start(setButton, False, True, padding=2)
        vMenuBox.pack_start(jonasButton, False, True, padding=2)
        self.pack_start(vMenuBox, False, False, padding=2)

        self.show()
        vMenuBox.show()
        rpc.register("add_hille", self.add_hille)

class SettingsPage(Page):
    def __init__(self, gui):
        super(SettingsPage, self).__init__("settings", gui, width="full")
        self.size_request = (300,300)
        button = create_menuButton("static/ikoner/arrow_left.png", "Tillbaka")
        button.connect("clicked", self.gui.switch_page, "menu")
        self.pack_start(button, False, False, padding=2)

        self.show_all()
        
class ContactPage(Page):
    def __init__(self, gui):
        super(ContactPage, self).__init__("contact", gui, width="full")
        self.size_request = (300,300)
        button = create_menuButton("static/ikoner/arrow_left.png", "Tillbaka")
        button.connect("clicked", self.gui.switch_page, "menu")
        self.pack_start(button, False, False, padding=2)

        self.show_all()
        
class MissionPage(Page):
  

    def __init__(self, gui):
        self.size_request = (300,300)
        super(MissionPage, self).__init__("mission", gui, homogeneous=False,spacing=0)
        newMissionButton = create_menuButton("static/ikoner/book_add.png","Lagg till")
        deleteMissionButton = create_menuButton("static/ikoner/book_delete.png","Ta bort")
        backButton = create_menuButton("static/ikoner/arrow_left.png","Tillbaka")
        
        backButton.connect("clicked", self.gui.switch_page, "menu")
        newMissionButton.connect("clicked", self.gui.switch_page, "addMission")
        deleteMissionButton.connect("clicked", self.gui.switch_page, "removeMission")
        self.pack_start(newMissionButton, False, False, padding=2)
        self.pack_start(deleteMissionButton, False, False, padding=2)
        self.pack_start(backButton, False, False, padding=2)

        self.show_all()

class AddMissionPage(Page):

    def __init__(self, gui):
        super(AddMissionPage, self).__init__("addMission", gui, homogeneous=False,
                spacing=0)
        self.size_request = (300,300)
        def dbupdate_press_callback(self, widget, data=None):   
            name = unicode(nameEntry.get_text())
            info = unicode(infoEntry.get_text())
            xEntry = unicode(xEntry.get_text())
            yEntry = unicode(yEntry.get_text())
            mission_save = str(packet.Packet("mission_save", name=name,\
                                info=info, xEntry=xEntry, yEntry=yEntry))
            print rpc.send("qos", "add_packet", packet=mission_save)
        
        nameLabel = gtk.Label("Namn:")
        nameEntry = gtk.Entry()
        infoLabel = gtk.Label("Info:")
        infoEntry = gtk.Entry()
        xLabel = gtk.Label("X-koordinat:")
        xEntry = gtk.Entry()
        yLabel = gtk.Label("Y-koordinat:")
        yEntry = gtk.Entry()
        okButton = gtk.Button("ok")
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
        self.pack_start(okButton, False, False,0)
        
        saveButton = create_menuButton("static/ikoner/disk.png","Spara")
        backButton = create_menuButton("static/ikoner/arrow_undo.png","Avbryt")
        backButton.connect("clicked", self.gui.switch_page, "mission")
        okButton.connect("clicked", dbupdate_press_callback, None)
        
        hbox1 = gtk.HBox()
        hbox1.pack_start(backButton, True, True, padding=2)
        hbox1.pack_start(saveButton, True, True, padding=2)
        self.pack_start(hbox1, False, False, 2)
        

        self.show_all()

class RemoveMissionPage(Page):

    def __init__(self, gui):
        super(RemoveMissionPage, self).__init__("removeMission", gui, homogeneous=False,
                spacing=0)
        self.size_request = (300,300)
        nameLabel = gtk.Label("Uppdrag:")
        selectBox = gtk.Combo()
        testList = ["Operation: Save the Whale", "Nuke Accident", "Brand i Sk?ggetorp"]
        selectBox.set_popdown_strings(testList)
        # TESTLIST SKA ERS?TTAS MED DATABAS-DATA

        
        self.pack_start(nameLabel, False, False,0)
        self.pack_start(selectBox, False, False,0)
        
        deleteButton = create_menuButton("static/ikoner/book_delete.png","Ta bort")
        backButton = create_menuButton("static/ikoner/arrow_undo.png","Avbryt")
        backButton.connect("clicked", self.gui.switch_page, "mission")
        
        hbox1 = gtk.HBox()
        hbox1.pack_start(backButton, True, True, padding=2)
        hbox1.pack_start(deleteButton, True, True, padding=2)
        self.pack_start(hbox1, False, False, 2)
        

        self.show_all()

class ObjectPage(Page):
    def checkNew(self, button, widget=None):
        self.gui._pages["addObject"].details(None, None, "show")
        self.gui.switch_page("addObject")

    def __init__(self, gui):
        super(ObjectPage, self).__init__("object", gui, homogeneous=False,
                spacing=0)
        self.size_request = (300,300)
        newButton = create_menuButton("static/ikoner/JonasInGlases.png",
                "Lagg till")
        deleteButton = create_menuButton("static/ikoner/JonasInGlases.png","Ta bort")
        backButton = create_menuButton("static/ikoner/JonasInGlases.png","Tillbaka")

        backButton.connect("clicked", self.gui.switch_page, "menu")
        newButton.connect("clicked", self.checkNew, None)
        deleteButton.connect("clicked", self.gui.switch_page, "removeObject")
        self.pack_start(newButton, False, False, padding=2)
        self.pack_start(deleteButton, False, False, padding=2)
        self.pack_start(backButton, False, False, padding=2)

        self.show_all()
        
class AddObjectPage(Page):

    def __init__(self, gui):
        super(AddObjectPage, self).__init__("addObject", gui, homogeneous=False,
                spacing=0)
        self.size_request = (300,300)
        hbox1 = gtk.HBox()
        vbox1 = gtk.VBox()
        self.vbox2 = gtk.VBox()
        nameLabel = gtk.Label("Namn:")
        self.nameEntry = gtk.Entry()
        objLabel = gtk.Label("Object:")
        self.objEntry = gtk.Entry()
        typeLabel = gtk.Label("Typ:")
        self.typeEntry = gtk.Entry()
        infoLabel = gtk.Label("Information:")
        infoEntry = gtk.Entry()
        xLabel = gtk.Label("X-koordinat:")
        self.xEntry = gtk.Entry()
        self.xEntry.set_editable(False)
        yLabel = gtk.Label("Y-koordinat:")
        self.yEntry = gtk.Entry()
        self.yEntry.set_editable(False)
        
        self.infoView = gtk.TextView(buffer=None)
        self.infoView.set_wrap_mode(gtk.WRAP_WORD)
        infoLabel = gtk.Label("Info:")
        self.infoView.set_size_request(300,200)
        #infoView = gtk.TextView(None)
        #infoView.set_editable(True)
        #infoTextBuffer = infoView.get_buffer()
        #infoScroll = gtk.ScrolledWindow()
        #infoScroll.set_size_request(294,150)
        #infoScroll.add(infoView)
        #infoScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        #infoView.set_wrap_mode(gtk.WRAP_WORD)
        
        vbox1.pack_start(nameLabel, False, False,0)
        vbox1.pack_start(self.nameEntry, False, False,0)
        vbox1.pack_start(objLabel, False, False,0)
        vbox1.pack_start(self.objEntry, False, False,0)
        vbox1.pack_start(typeLabel, False, False,0)
        vbox1.pack_start(self.typeEntry, False, False,0)
        vbox1.pack_start(xLabel, False, False,0)
        vbox1.pack_start(self.xEntry, False, False,0)
        vbox1.pack_start(yLabel, False, False,0)
        vbox1.pack_start(self.yEntry, False, False,0)
        
        saveButton = create_menuButton("static/ikoner/disk.png","Spara")
        backButton = create_menuButton("static/ikoner/arrow_undo.png","Avbryt")
        self.showDetails = create_menuButton("static/ikoner/resultset_first.png","Visa Detaljer")
        self.hideDetails = create_menuButton("static/ikoner/resultset_last.png","Goem Detaljer")

        backButton.connect("clicked", self.gui.switch_page, "object")

        self.showDetails.connect("clicked", self.details, "show")
        self.hideDetails.connect("clicked", self.details, "hide")
        saveButton.connect("clicked", self.send_object)
        
        hbox2 = gtk.HBox()
        hbox2.pack_start(backButton, True, True, padding=2)
        hbox2.pack_start(saveButton, True, True, padding=2)
        
        vbox1.pack_start(hbox2, False, False, 2)
        vbox1.pack_start(self.showDetails,False,False,2)
        vbox1.pack_start(self.hideDetails,False,False,2)
        hbox1.pack_start(vbox1,True,True,2)
        self.vbox2.pack_start(infoLabel,False,False,0)
        self.vbox2.pack_start(self.infoView,False,False,0)
        hbox1.pack_start(self.vbox2,False,False,0)
        self.pack_start(hbox1,False,False,0)
        self.show_all()
        self.vbox2.hide()
        self.hideDetails.hide()
        self.infoView.hide()

    def send_object(self, button):
        #lägg till så man kan fixa in sub_type
        poi = str(packet.Packet("poi",id = "", sub_type = "", name = self.nameEntry.get_text(), coordx = self.xEntry.get_text(), coordy = self.yEntry.get_text()))
        rpc.send("qos", "add_packet", packet=poi)
    
    def map_dblclick(self, coordx, coordy):
        print "Jon bajsar!"
        self.xEntry.set_text(str(coordx))
        self.yEntry.set_text(str(coordy))
        
    def details(self, button, state, widget=None):
        if state == "show":
            self.gui.rightBook.set_size_request(600,300)
            self.vbox2.show()
            self.showDetails.hide()
            self.hideDetails.show()
        elif state == "hide":
            self.gui.rightBook.set_size_request(300,300)
            self.vbox2.hide()
            self.showDetails.show()
            self.hideDetails()

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
        self._pages["contact"] = SettingsPage(self)
        self._pages["addMission"] = AddMissionPage(self)
        self._pages["removeMission"] = RemoveMissionPage(self)
        self._pages["object"] = ObjectPage(self)
        self._pages["addObject"] = AddObjectPage(self)

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
