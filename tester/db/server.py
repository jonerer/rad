# coding: utf-8
from shared.data import get_session, create_tables
from shared.data.defs import *

session = get_session() # för default-databasen
session = get_session("sqlite:///server/db.db")

# generates an example server db.
create_tables()

# Ritar ut tre objekt
print "den här ska skapa en exempel-databas till servern, men inget e fixat än"
# stoppa in de här unitsen i server-databasen
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

