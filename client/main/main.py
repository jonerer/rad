#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
import thread
import time
import sys
import os
import gui
import data_storage
import map_xml_reader
from shared import data, rpc
#from shared import data
from shared.data import get_session, create_tables
from shared.data.defs import *

if sys.version_info[1] == 3:
    print "nu glömde du skriva python2.5... trooooooliiiigt"
    sys.exit(0)

rpc.set_name("main")

print "Läser in kartinformation från static/kartdata/map.xml"
        
# Kartan
mapxml = map_xml_reader.MapXML("static/kartdata/map.xml")

map = data_storage.MapData(mapxml.get_name(),
                           mapxml.get_levels())
map.set_focus(15.5726, 58.4035)
print "gör session"
session = get_session()
print "gör tables"
create_tables()
session.query(Unit).all()
session.query(UnitType).all()
#Om du behöver fylla på databasen igen gör dessa nedanför
#skapar olika unittypes
#a=UnitType(u"Ambulans1", "static/ikoner/ambulans.png")
#b=UnitType(u"Brandbild1", "static/ikoner/brandbil.png")
#c=UnitType(u"sjukhus1", "static/ikoner/sjukhus.png")
#d=UnitType(u"jonas","static/ikoner/JonasInGlases.png")
#session.add(b)
#session.add(c)
#session.add(d)
#session.add(a)
#session.commit()
#skapar användarna
#session.add(Unit(u"hej", a, 15.57796, 58.40479))
#session.add(Unit(u"ho", a, 15.57806, 58.40579))
#session.add(Unit(u"lets", b, 15.5729, 58.40193))
#session.add(Unit(u"go", c, 15.5629, 58.4093))
#session.add(Unit(u"III", d, 15.5829, 58.4093, True))
#session.commit()

#Ritar ut alla objekt i databasen
for units in session.query(Unit).all():
    map.add_object(units.name, data_storage.MapObject(
        {"longitude":units.coordx,"latitude":units.coordy},
        units.type.image))

# Ritar ut tre objekt
#map.add_object("Ambulans1", data_storage.MapObject(
#    {"longitude":15.57796,"latitude":58.40479},
#    "static/ikoner/ambulans.png"))
#map.add_object("Ambulans2", data_storage.MapObject(
#    {"longitude":15.57806, "latitude":58.40579},
#    "static/ikoner/ambulans.png"))
#map.add_object("Brandbil1", data_storage.MapObject(
#    {"longitude":15.5729,"latitude":58.40193},
#    "static/ikoner/brandbil.png"))
#map.add_object("Sjukhus1", data_storage.MapObject(
#    {"longitude":15.5629, "latitude":58.4093},
#    "static/ikoner/sjukhus.png"))
#map.add_object("jonas", data_storage.MapObject(
#    {"longitude":15.5829,"latitude":58.4093},
#    "static/ikoner/JonasInGlases.png", True))

#map.add_object("Shape1", data_storage.MapObject({"longitude":15.5829,
#                                                 "latitude":58.4093},
#                                                "arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
#                                                "set_source_rgb(0, 0, 0)"))
# Skapar grafiska interfacet.
print "Skapar programmets GUI"
app = gui.Gui(map)

# Kör programmet
print "Kör programmet."
app.run()

