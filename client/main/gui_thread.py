# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui

def run():
    print "Läser in kartinformation från kartdata/map.xml"
            
    # Kartan
    mapxml = map_xml_reader.MapXML("static/kartdata/map.xml")

    map = data_storage.MapData(mapxml.get_name(),
                               mapxml.get_levels())

    # Ställer in vad kartkomponenten ska fokusera på (visa)
    # (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-lyd.
    map.set_focus(15.5726, 58.4035)

    # Ritar ut tre objekt
    map.add_object("Ambulans1", data_storage.MapObject(
        {"longitude":15.57796,"latitude":58.40479},
        "ikoner/ambulans.png"))
    map.add_object("Ambulans2", data_storage.MapObject(
        {"longitude":15.57806, "latitude":58.40579},
        "ikoner/ambulans.png"))
    map.add_object("Brandbil1", data_storage.MapObject(
        {"longitude":15.5729,"latitude":58.40193},
        "ikoner/brandbil.png"))
    map.add_object("Sjukhus1", data_storage.MapObject(
        {"longitude":15.5629, "latitude":58.4093},
        "ikoner/sjukhus.png"))

    map.add_object("Shape1", data_storage.MapObject({"longitude":15.5829,
                                                     "latitude":58.4093},
                                                    "arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
                                                    "set_source_rgb(0, 0, 0)"))

    # Skapar grafiska interfacet.
    print "Skapar programmets GUI."
    app = gui.Gui(map)

    # Kör programmet
    print "Kör programmet."
    app.run()
