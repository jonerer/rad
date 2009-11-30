# -*- coding: utf-8 -*-
import gtk
import math
import time
import data_storage
import gui
from shared import packet
from shared import rpc
from datetime import datetime
from shared.data import get_session, create_tables
from shared.data.defs import *
#from tester.osso import rpc

class Map(gtk.DrawingArea):
    _bounds = {"min_latitude":0,
                "max_latitude":0,
                "min_longitude":0,
                "max_longitude":0}

    def __init__(self, map, gui):
        gtk.DrawingArea.__init__(self)
        
        # Variabler
        self._map = map
        self._pos = {"x":0, "y":0}
        self._origin_position = None
        self._cols = 0
        self._rows = 0
        self._gps_data = None
        self._movement_from = {"x": 0, "y":0}
        self._allow_movement = False
        self._last_movement_timestamp = 0.0
        self._zoom_level = 1
        self._is_dirty = True
        self._last_tiles = None
        self._last_focus_pixel = 0,0
        self._focus_pixel = 0,0
        self._last_click = datetime.now()
        self._gui = gui
        self._width = None
        self._height = None

        rpc.register("update_items", self.update_items)
        
        rpc.register("ping_with_coordinates", self.update_units)
        rpc.register("update_map", self.force_draw)
        # queue_draw() ärvs från klassen gtk.DrawingArea
        map.set_redraw_function(self.queue_draw)
      
        self.connect("expose_event", self.handle_expose_event)
        self.connect("button_press_event", self.handle_button_press_event)
        self.connect("button_release_event", self.handle_button_release_event)
        self.connect("motion_notify_event", self.handle_motion_notify_event)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)

    def update_items(self, items):
        # receive a dict describing db updates from server
        print "ska uppdateras:"
        for item in items:
            print item
    
    def change_zoom(self, change):
        
        # Frigör minnet genom att ladda ur alla tiles för föregående nivå
        level = self._map.get_level(self._zoom_level)
        level.unload_tiles("all")
      
        if change == "+":
            if self._zoom_level < 3:
                self._zoom_level += 1
        else:
            if self._zoom_level > 1:
                self._zoom_level -= 1

        # Ritar ny nivå
        self._is_dirty = True
        self.queue_draw()

    # Hanterar rörelse av kartbilden
    def handle_button_press_event(self, widget, event):
        import data_storage
        self._movement_from["x"] = event.x
        self._movement_from["y"] = event.y
        self._origin_position = self._map.get_focus()
        self._last_movement_timestamp = time.time()
        self._allow_movement = True

        return True

    def handle_button_release_event(self, widget, event):
        self._allow_movement = False
        self._is_dirty = True
        self.queue_draw()

        if time.time() < self._last_movement_timestamp + 0.1:
            #event.xcoord, event.ycoord = self.pixel_to_gps(event.x, event.y)
            lon, lat = self.pixel_to_gps(event.x-self._width/2, event.y-self._height/2)
            lon = self._origin_position["longitude"] + lon
            lat = self._origin_position["latitude"] - lat
            

            self._gui.map_dblclick(lon, lat)
            self.red_dot(lon,lat)
            print "coords lon,lat: %s,%s" % (lon, lat)
            #session.add(POI(15.57806, 58.40579, 2, u"ho", a, datetime.now()))
            #self._map.add_object("skonaste", data_storage.MapObject(
            #    {"longitude":lon,"latitude":lat},
            #    "static/ikoner/brandbil.png"))    
            #self._gui.map_dblclick(widget, event)
        return True

    def handle_motion_notify_event(self, widget, event):
        if self._allow_movement:
            if event.is_hint:
                x, y, state = event.window.get_pointer()
            else:
                x = event.x
                y = event.y
                state = event.state

            # Genom tidskontroll undviker vi oavsiktlig rörelse av kartan,
            # t ex ifall någon råkar nudda skärmen med ett finger eller liknande.
            if time.time() > self._last_movement_timestamp + 0.1:
                lon, lat = self.pixel_to_gps(self._movement_from["x"] - x,
                                             self._movement_from["y"] - y)
                self._map.set_focus(self._origin_position["longitude"] + lon,
                                     self._origin_position["latitude"] - lat)
                self._focus_pixel = (self._movement_from["x"] - x,
                    self._movement_from["y"] - y)
                self._movement_from["x"] = x
                self._movement_from["y"] = y
            
                # Ritar om kartan. eller?
        #self._is_dirty = True
                #self.queue_draw()

        return True

    def handle_expose_event(self, widget, event):
    # den här kallas samtidigt om queue_draw verkar d som.
        self.context = widget.window.cairo_create()

    # skapa en pixbuf och lägg den i minnet.
    # bara en gång.
    #if not hasattr(self, "_pixbuf"):
    #   self._pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, \
    #           False, 8, event.area.width, event.area.height)

        # Regionen vi ska rita på
        self.context.rectangle(event.area.x,
                               event.area.y,
                               event.area.width,
                               event.area.height)
        self._width = event.area.width
        self._height = event.area.height
        self.context.clip()
    
        self.draw()

        return False

    def set_gps_data(self, gps_data):
        self._gps_data =  gps_data
        self._is_dirty = True

    def force_draw(self):
        self._is_dirty = True
        self.queue_draw()

    def draw(self):
        if self._is_dirty:
            # Hämtar alla tiles för en nivå
            level = self._map.get_level(self._zoom_level)
            # Plockar ur de tiles vi söker från nivån
            tiles, cols, rows = level.get_tiles(self._map.get_focus())
            self._cols = cols
            self._rows = rows

            self._bounds["min_longitude"] = tiles[0].bounds["min_longitude"]
            self._bounds["min_latitude"] = tiles[0].bounds["min_latitude"]
            self._bounds["max_longitude"] = tiles[-1].bounds["max_longitude"]
            self._bounds["max_latitude"] = tiles[-1].bounds["max_latitude"]

            self._is_dirty = False
            self._last_focus_pixel = self._focus_pixel
            self._last_tiles = tiles
        else:
            # here, don't redraw the whole map, just move it around.
            tiles = self._last_tiles
            pixel_focus_diff =  self._focus_pixel[0] - self._last_focus_pixel[0], \
                self._focus_pixel[1] - self._last_focus_pixel[1]
                
        # Ritar kartan
        for tile in tiles:
            #img = tile.get_picture()
            x, y = self.gps_to_pixel(tile.bounds["min_longitude"],
                         tile.bounds["min_latitude"])
            tile.draw(self.context, x, y)

        # Ritar ut eventuella objekt
        objects = self._map.get_objects()
        for item in objects:
            x, y = self.gps_to_pixel(item["object"].get_coordinate()["longitude"],
                         item["object"].get_coordinate()["latitude"])
            if x != 0 and y != 0:
                item["object"].draw(self.context, x, y)
   
    def gps_to_pixel(self, lon, lat):
        cols = self._cols
        rows = self._rows
        width = self._bounds["max_longitude"] - self._bounds["min_longitude"]
        height = self._bounds["min_latitude"] - self._bounds["max_latitude"]
      
        # Ger i procent var vi befinner oss på width och height
        where_lon = (lon - self._bounds["min_longitude"]) / width
        where_lat = (self._bounds["min_latitude"] - lat) / height
      
        # Ger i procent var focus befinner sig på width och height
        where_focus_lon = (self._map.get_focus()["longitude"] - \
                           self._bounds["min_longitude"]) / width
        where_focus_lat = (self._bounds["min_latitude"] - \
                           self._map.get_focus()["latitude"]) / height
      
        # Placerar origo i skärmens centrum
        rect = self.get_allocation()
        x = rect.width / 2.0
        y = rect.height / 2.0
      
        # Räknar ut position:
        x += (where_lon - where_focus_lon) * (cols * 300.0)
        y += (where_lat - where_focus_lat) * (rows * 160.0)
      
        return [round(x), round(y)]
   
    def pixel_to_gps(self, movement_x, movement_y):
        # Hämtar alla tiles för en nivå
        level = self._map.get_level(self._zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self._map.get_focus())
      
        # Gps per pixlar
        width = self._bounds["max_longitude"] - self._bounds["min_longitude"]
        height = self._bounds["min_latitude"] - self._bounds["max_latitude"]
        gps_per_pix_width = width / (cols * 300)
        gps_per_pix_height = height / (rows * 160)
      
        # Observera att kartans GPS-koordinatsystem börjar i vänstra nedre
        # hörnet, medan cairo börjar i vänstra övre hörnet! På grund av detta
        # inverterar vi värdet vi räknar fram så båda koordinatsystemen
        # överensstämmer.
        return [gps_per_pix_width * movement_x,
                gps_per_pix_height * movement_y]

    def red_dot(self, dotx, doty):
        objList = self._map.get_objects()
        hit = False
        list = self.pixel_to_gps(32,32)
        unit = None
        for obj in objList:
            print obj
            value = obj["object"]
            valueTwo = value.get_coordinate()
            sideTop = valueTwo["latitude"]
            sideLeft = valueTwo["longitude"]
            sideRight = valueTwo["longitude"]+list[0]
            sideBottom = valueTwo["latitude"]-list[1]
            if doty > sideBottom and doty < sideTop and dotx < sideRight and dotx > sideLeft:
                print "hit! "
                hit = True
                unit = obj["id"]
                self._gui.show_object(obj)
                self._map.set_focus(dotx,doty)
                
        self._map.delete_object(u"dot")
        
        if hit == False:
        
            self._map.add_object(u"dot", data_storage.MapObject({"longitude":dotx-(list[0]/2),"latitude":doty+(list[1]/2)},"static/ikoner/add.png"))
            self.queue_draw()
            poi.coordx = dotx
            poi.coordy = doty
            session.commit()
        self._map.add_object(u"dot", data_storage.MapObject({"longitude":dotx,"latitude":doty},"static/ikoner/JonasInGlases.png"))
        self.self.queue_draw()

    def update_units(self,lon,lat,pack=None):
        print "update_units"
        session = get_session()
        if pack == None:
            for units in session.query(Unit).filter(Unit.is_self==True):
                print "Ditt unit name: ", units.name
                update_unit = self._map.get_object(units.id)
                print "Ditt object map är :",update_unit
                update_unit["object"].make_dict(lon,lat)
        else:
            pack = packet.Packet.from_str(pack)
            print pack.data["name"]
            print pack.data["lon"]
            print pack.data["lat"]
            for units in session.query(Unit).filter(Unit.name==pack.data["name"]):
                print units
                update_unit = self._map.get_object(units.id)
                update_unit["object"].make_dict(pack.data["lon"],pack.data["lat"],pack.data["name"])
        self.queue_draw()
