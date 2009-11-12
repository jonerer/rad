# coding: utf-8
from shared.data import get_session, create_tables
from shared.data.defs import *
from sqlalchemy.sql import exists

session = get_session() # för default-databasen
session = get_session("sqlite:///client/db.db")

# generates an example server db.
create_tables()

# Ritar ut tre objekt
# stoppa in de här unitsen i server-databasen
if len(session.query(UnitType).all()):
    print "Databasfilen client/db.db e inte tom. Ta bort den först om du"+\
            " vill att ja ska trycka in exempeldatan."
    import sys
    sys.exit(0)
ambul = UnitType(u"Ambulans", "ambulans.png")
brand = UnitType(u"Brandbil", "brandbil.png")
sjukh = UnitType(u"Sjukhus", "sjukhus.png")

session.add(ambul)
session.add(brand)
session.add(sjukh)
print session.query(UnitType).all()

session.add(Unit(u"Ambulans1", ambul, 15.57796, 58.40479))
session.add(Unit(u"Ambuls2", ambul, 15.57806, 58.40579))
session.add(Unit(u"Brandbilen", brand, 15.5729, 58.40193))
session.add(Unit(u"sjukis", sjukh, 15.5629, 58.4093))
session.add(Unit(u"self", brand, 15.5829, 58.4093, True))
print session.query(Unit).all()
session.commit()


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

