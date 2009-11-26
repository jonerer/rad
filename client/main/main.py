#!/usr/bin/python2.5
# -*- coding: utf-8 -*
import thread
import time
import sys
import os
import gui
import data_storage
import map_xml_reader
from shared import data, rpc
from shared.data import get_session, create_tables
from shared.data.defs import *
import logging
import subprocess
from datetime import datetime

if sys.version_info[1] == 3:
    print "nu glömde du skriva python2.5... trooooooliiiigt"
    sys.exit(0)

rpc.set_name("main")

# Kartan
mapxml = map_xml_reader.MapXML("static/kartdata/map.xml")

map = data_storage.MapData(mapxml.get_name(),
                           mapxml.get_levels())
map.set_focus(15.5726, 58.4035)
session = get_session()
create_tables()
units = session.query(Unit).all()
types = session.query(UnitType).all()

if "exempeldata" in sys.argv and len(types) == 0:

    sjukhus = POIType(u"sjukhus1", "static/ikoner/sjukhus.png")
    session.add(sjukhus)

    #Lägger till alla poi's
    session.add(POI(15.6001709, 58.40533172, 4, u"Sjukhus", sjukhus, datetime.now()))

    #UnitTypes

    ambulans = UnitType(u"Ambulans1", "static/ikoner/ambulans.png")
    brandbil = UnitType(u"Brandbild1", "static/ikoner/brandbil.png")
    jonas = UnitType(u"jonas","static/ikoner/JonasInGlases.png")
    session.add(ambulans)
    session.add(brandbil)
    session.add(jonas)

    #skapar units
    session.add(Unit(u"Ambulans ett", ambulans, 15.5829, 58.4093, False))
    session.add(Unit(u"Ambulans två", ambulans, 15.57806, 58.40579, False))
    session.add(Unit(u"Brandbil", brandbil, 15.5729, 58.40193, False))
    session.add(Unit(u"Fotgängare", jonas, 15.5720, 58.4026, False))

    session.commit()
    #skapar en POI-type
    #self, coordx, coordy, id, name, sub_type, timestamp

else:
    # kolla att man har nått i databasen
    num_types = len(types)
    if not num_types:
        logging.warn("du har inget i databasen. kör"+\
                "'./start main exempeldata' för o dra in lite exempeldata.")
    elif "exempeldata" in sys.argv:
        logging.warn("du försökte exempeldata, men hade redan saker i"+\
                "databasen. ta bort den först för att tömma.")

#Ritar ut alla objekt i databasen
for units in session.query(Unit).all():
    map.add_object(units.name, data_storage.MapObject(
        {"longitude":units.coordx,"latitude":units.coordy},
        units.type.image, units.is_self))
for poi in session.query(POI).all():
    map.add_object(poi.name, data_storage.MapObject(
        {"longitude":poi.coordx,"latitude":poi.coordy},
        poi.type.image))

# Skapar grafiska interfacet.
print "Skapar programmets GUI"
app = gui.Gui(map)

# Kör programmet
print "Kör programmet."
app.run()

