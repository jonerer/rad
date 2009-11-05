# -*- coding: utf-8 -*-
import time
import gtk
import struct
import math
from shared import rpc

# Tar reda på en PNG-bilds storlek
def png_size(path):
    stream = open(path, "rb")

    # Dummy read to skip header data
    stream.read(12)
    if stream.read(4) == "IHDR":
        (x, y) = struct.unpack("!LL", stream.read(8))
        error = "no error"

    return (x, y, error)

# Ger en lista med snittet mellan två listor
def intersection(list1, list2):
    int_dict = {}
    list1_dict = {}

    for e in list1:
        list1_dict[e.name] = e
    for e in list2:
        if list1_dict.has_key(e.name):
            int_dict[e.name] = e

    return int_dict.values()

# Ger en lista med unionen mellan två listor
def union(list1, list2):
    union_dict = {}
    for e in list1:
        union_dict[e.name] = e
    for e in list2:
        union_dict[e.name] = e

    return union_dict.values()

class Picture(object):
    _path_to_picture = None
    _picture = None
    _commands = None

    def set_path_to_picture(self, path):
        self._path_to_picture = path

    def get_path_to_picture(self):
        return self._path_to_picture

    def draw_shapes(self, context, x, y, commands):
        for cmd in commands:
            eval('context.'+cmd)
        context.stroke()

    def draw_picture(self, context, x, y):
        context.set_source_pixbuf(self.get_picture(), x, y)
        context.paint()

    def draw(self, context, x, y):
        if self.get_path_to_picture():
            self.draw_picture(context, x, y)
        else:
            self.draw_shapes(context, x, y, self.get_commands())

    def set_commands(self, commands):
        self._commands = commands

    def get_commands(self):
        return self._commands

    def load_picture(self):
        self._picture = gtk.gdk.pixbuf_new_from_file(self.get_path_to_picture())

    def unload_picture(self):
        self._picture = None        

    def get_picture(self):
        if self._picture:
            return self._picture
        else:
            self.load_picture()
            return self._picture

# Lagrar en kartbild och dess koordinatavgränsningar
class MapTile(Picture):
    _type = None

    def set_type(self, type):
        self._type = type

    def get_type(self):
        return self._type

    def __init__(self, id, path, bounds, type):
        self.name = id
        self.set_path_to_picture(path)
        self.bounds = bounds
        self.set_type(type)

# Lagrar alla MapTiles (kartbilder)
class Tiles(object):
    # Håller reda på vilket område samtliga tiles omfattar
    _bounds = {"min_latitude":None,
                "max_latitude":None,
                "min_longitude":None,
                "max_longitude":None}

    # Lagrar alla tiles
    _tiles = None

    def get_cols(self):
        return self._cols

    def get_rows(self):
        return self._rows

    def __init__(self, width, height):
        # Lagrar basbildens bredd och höjd
        self._width = int(width)
        self._height = int(height)
        
        # Behövs för att lägga in tiles
        self._col_pos = 0
        self._row_pos = 0
    
        # Behövs för matematiska beräkningar
        self._cols = 0
        self._rows = 0

    def update_bounds(self, bounds):
        if self._bounds["min_latitude"] == None:
            self._bounds["min_latitude"] = bounds["min_latitude"]
        elif bounds["min_latitude"] > self._bounds["min_latitude"]:
            self._bounds["min_latitude"] = bounds["min_latitude"]

        if self._bounds["max_latitude"] == None:
            self._bounds["max_latitude"] = bounds["max_latitude"]
        elif bounds["max_latitude"] < self._bounds["max_latitude"]:
            self._bounds["max_latitude"] = bounds["max_latitude"]

        if self._bounds["min_longitude"] == None:
            self._bounds["min_longitude"] = bounds["min_longitude"]
        elif bounds["min_longitude"] < self._bounds["min_longitude"]:
            self._bounds["min_longitude"] = bounds["min_longitude"]

        if self._bounds["max_longitude"] == None:
            self._bounds["max_longitude"] = bounds["max_longitude"]
        elif bounds["max_longitude"] > self._bounds["max_longitude"]:
            self._bounds["max_longitude"] = bounds["max_longitude"]

    def create_empty_tiles(self, cols, rows):
        self._cols = cols
        self._rows = rows
        self._tiles = [[[] for ni in range(rows)] for mi in range(cols)]

    def get_bounds(self):
        return self._bounds

    def add_tile(self, tile):
        self.update_bounds(tile.bounds)
        self._tiles[self._col_pos][self._row_pos] = tile

        if tile.get_type() == "end":
            self._row_pos += 1
            self._col_pos = 0
        else:
            self._col_pos += 1

    # Laddar ur tiles för att frigöra minnet
    def unload_tiles(self, tiles_list):
        if tiles_list == "all":
            tiles_list = self._tiles

        for tiles in tiles_list:
            for tile in tiles:
                tile.unload_picture()

    # Hämtar alla tiles som ligger inom ett avgränsat koordinatområde
    # Kom ihåg att latitude växer från botten mot toppen, inte tvärtom. Dock
    # kallas topppen för min_latitude.
    def get_tiles(self, focus):
        gps_width = self._bounds["max_longitude"] - \
                    self._bounds["min_longitude"]
        gps_height = self._bounds["min_latitude"] - \
                     self._bounds["max_latitude"]

        # Skärmen på N810:an är 800x480.
        width = (gps_width / self._width) * 400
        height = (gps_height / self._height) * 240

        bounds = {"min_longitude":(focus["longitude"] - width),
                  "max_longitude":(focus["longitude"] + width),
                  "min_latitude":focus["latitude"] + height,
                  "max_latitude":focus["latitude"] - height}

        # Undviker att vi hamnar utanför det område tiles:en täcker
        if bounds["min_longitude"] < self._bounds["min_longitude"]:
            bounds["min_longitude"] = self._bounds["min_longitude"]

        if bounds["max_longitude"] > self._bounds["max_longitude"]:
            bounds["max_longitude"] = self._bounds["max_longitude"]

        if bounds["min_latitude"] > self._bounds["min_latitude"]:
            bounds["min_latitude"] = self._bounds["min_latitude"]

        if bounds["max_latitude"] < self._bounds["max_latitude"]:
            bounds["max_latitude"] = self._bounds["max_latitude"]

        start_lon = bounds["min_longitude"] - self._bounds["min_longitude"]
        stop_lon = bounds["max_longitude"] - self._bounds["min_longitude"]
        start_lat = self._bounds["min_latitude"] - bounds["min_latitude"]
        stop_lat = self._bounds["min_latitude"] - bounds["max_latitude"]

        # Det bästa sättet att förstå matematiken nedanför är att rita upp ett
        # rutnät med alla tiles, dvs x * y, t ex 3x5. Börja sedan räkna på
        # matematiken nedan utifrån rutnätet. I enkelhet handlar det nedan
        # om att räkna ut i procent var vi befinner oss i x-led och y-led
        # och sedan gångra denna procent med antalet kolumner och rader vi har,
        # och på så vis få reda på vilka rutor som ska visas.
        # Algoritmen är inte på något vis perfekt och bättre lösningar finns
        # säkert.
        x_start = int(math.floor(self._cols * (start_lon / gps_width)))
        x_stop = int(math.ceil(self._cols * (stop_lon / gps_width)))
        if x_stop == self._cols:
            x_stop -= 1 # Så vi inte överskrider max antalet tiles i x-led.

        y_start = int(math.floor(self._rows * (start_lat / gps_height)))
        y_stop = int(math.ceil(self._rows * (stop_lat / gps_height)))
        if y_stop == self._rows:
            y_stop -= 1 # Så vi inte överskrider max antalet tiles i y-led.

        # Frigör minne genom att ladda ur de tiles som inte visas
        tiles_left = []
        if x_start - 1 >= 0:
            self.unload_tiles(self._tiles[0:x_start])

        tiles_right = []
        if x_stop + 1 != self._cols:
            self.unload_tiles(self._tiles[x_stop:self._cols])

        # Returnerar de tiles som efterfrågas
        tiles = self._tiles[x_start:x_stop + 1]
        result = []
        for tile in tiles:
            result += tile[y_start:y_stop + 1]

        return [result,
                x_stop + 1 - x_start,
                y_stop + 1 - y_start]

# Datastruktur som lagrar kartans bild och de generella objekt som ska ritas ut
# på denna. Med generella objekt menas objekt som hela tiden ska vara på kartan,
# som ej försvinner när exempelvis ett uppdrag avslutats.
class MapData(object):
    _objects = []
    _mission_objects = []
    _levels = {}
    _redraw_function = None
    _focus = {"latitude":0,
               "longitude":0}

    # name är namnet på kartan, t ex Ryd.
    # levels är tre stycken Tiles-objekt.
    def __init__(self, name, levels):
        self.name = name
        self.set_level(1, levels[1])
        self.set_level(2, levels[2])
        self.set_level(3, levels[3])
        self.bounds = levels[1].get_bounds()

    # Ställer in Tiles-objekt för en bestämd nivå
    def set_level(self, level, tiles):
        self._levels[level] = tiles

    # Returnerar ett Tiles-objekt för en given nivå
    def get_level(self, level):
        return self._levels[level]

    def set_focus(self, longitude, latitude):
        self._focus["longitude"] = longitude
        self._focus["latitude"] = latitude
        self.redraw()

    def get_focus(self):
        return self._focus

    def remove_objects(self):
        self._objects = []

    def add_object(self, object_id, map_object):
        self._objects.append({"id":object_id,
                               "object":map_object})

    def delete_object(self, object_id):
        for item in self._objects:
            if item["id"] == object_id:
                self._objects.remove(item)

    def get_object(self, object_id):
        for item in self._objects:
            if item["id"] == object_id:
                return self._objects[item]

    def get_objects(self):
        return self._objects

    def set_redraw_function(self, redraw_function):
        self._redraw_function = redraw_function

    def redraw(self):
        if self._redraw_function:
            self._redraw_function()

# Är den typen av objekt som lagras i MapData. T ex en ambulans som ska visas
# på kartan eller "blockerad väg"-symbol.
class MapObject(Picture):
    _coordinate = None

    # coordinate-variabeln är en dict enligt
    # {"latitude":float, "longitude":float}
    # type är objektets typ, anges med siffra. Kan vara en ambulans, polisbil,
    # ett träd eller vad man nu hittar på.
    def __init__(self, coordinate, path, is_self=False):
        self.set_coordinate(coordinate)
        #call set_coordinate to update self pos
        #if self=true makes u update the object position
        if is_self:
            rpc.register("ping_with_coordinates", self.make_dict)

#        if len(path) == 1:
        self.set_path_to_picture(path)
#        else:
#            self.set_commands(path)
            
    #Make dict to sen to set_coordinate
    def make_dict(self, lon, lat):
        dict = {"longitude":lon,"latitude":lat}
        self.set_coordinate(dict)
        
    def set_coordinate(self, coordinate):
        self._coordinate = coordinate

    def get_coordinate(self):
        return self._coordinate

    def set_visible(self, visible):
        self._visible = visible

    def get_visible(self):
        return self._visible
