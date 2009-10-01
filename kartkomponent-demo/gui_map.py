# -*- coding: utf-8 -*-
import gtk
import math
import time

class Map(gtk.DrawingArea):
    _bounds = {"min_latitude":0,
                "max_latitude":0,
                "min_longitude":0,
                "max_longitude":0}

    def __init__(self, map):
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
        self._pixbuf = None
        self._blank_buf = None
        
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
        if self._pixbuf == None:
            self._pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, \
                    True, 8, event.area.width, event.area.height)

        # Regionen vi ska rita på
        self.context.rectangle(event.area.x,
                               event.area.y,
                               event.area.width,
                               event.area.height)
        self.context.clip()
    
        self.draw()

        return False

    def set_gps_data(self, gps_data):
        self._gps_data =  gps_data
        self._is_dirty = True

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

            self._pixbuf.fill(0xffffffff)
            # försöka få tag på en pixbuf eller nått att rita på?
            # Ritar kartan
            target_width = self._pixbuf.get_width()
            target_height = self._pixbuf.get_height()
            for tile in tiles:
                #img = tile.get_picture()
                x, y = self.gps_to_pixel(tile.bounds["min_longitude"],
                             tile.bounds["min_latitude"])
                x, y = int(x), int(y)
                tile.draw(self.context, x, y)
                #pixbuf-grejen: funkar inte, tror den försöker kopiera utanför målet
                tile_pic = tile.get_picture()
                #print tile_pic.get_width()
                #print self._pixbuf.get_width()

                x_draw = x
                x_clip = 0
                x_clip_width = tile_pic.get_width()
                y_clip = 0
                y_draw = y
                y_clip_width = tile_pic.get_height()
                #if y_clip_width > target_height:
                #    print "FUKKEN FAILD"
                if x < 0:
                    x_clip = -x
                    x_draw = 0
                    x_clip_width -= x_clip
                if x_clip_width + x_draw > target_width:
                    x_clip_width = target_width - x_draw
                if y < 0:
                    y_clip = -y
                    y_draw = 0
                    y_clip_width -= y_clip
                if y_clip_width + y_draw > target_height:
                    y_clip_width = target_height - y_draw
                #print "y:",y_clip, y_draw, y_clip_width, tile_pic.get_height()
                #print "x:",x_clip, x_draw, x_clip_width, tile_pic.get_width()
                #if x_clip or y_clip or y_clip_width != tile_pic.get_width() \
                #        or y_clip_width != tile_pic.get_height():
                #    tile_pic = tile_pic.subpixbuf(x_clip, y_clip, x_clip_width, y_clip_width)
                
                #def copy_area(src_x, src_y, width, height, dest_pixbuf, dest_x, dest_y)
                #def subpixbuf(src_x, src_y, width, height)
                # first, create a temp pixbuf.
                tile_pic.copy_area(x_clip, y_clip, x_clip_width, y_clip_width, \
                    self._pixbuf, x_draw, y_draw)
                self._old_pixbuf = self._pixbuf.copy()
                self._move_since_clean = (0,0)
        else:
            # here, don't redraw the whole map, just move it around.
            pixel_focus_diff =  self._focus_pixel[0] - self._last_focus_pixel[0], \
                self._focus_pixel[1] - self._last_focus_pixel[1]
            self._move_since_clean = \
                    (pixel_focus_diff[0]+self._move_since_clean[0],
                    pixel_focus_diff[1]+self._move_since_clean[1])

            pixel_focus_diff = self._move_since_clean
            if pixel_focus_diff[0] != 0 or pixel_focus_diff[1] != 0:
                x_src = 0
                y_src = 0
                width = self._pixbuf.get_width()
                height = self._pixbuf.get_height()
                x_to = 0
                y_to = 0
                if pixel_focus_diff[0] < 0:
                    x_to = -pixel_focus_diff[0]
                    width += pixel_focus_diff[0]
                else:
                    x_src = pixel_focus_diff[0]
                    width -= pixel_focus_diff[0]
                if pixel_focus_diff[1] < 0:
                    y_to = -pixel_focus_diff[1]
                    height += pixel_focus_diff[1]
                else:
                    y_src = pixel_focus_diff[1]
                    height -= pixel_focus_diff[1]
                #print x_src, y_src, width, height, x_to, y_to
                self._old_pixbuf.copy_area(int(x_src), int(y_src), \
                        int(width), int(height), \
                        self._pixbuf, int(x_to), int(y_to))

        # till pixbuf-lösningen:
        self.context.set_source_pixbuf(self._pixbuf, 0, 0)
        self.context.paint()
        
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
