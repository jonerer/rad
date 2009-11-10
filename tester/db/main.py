# coding: utf-8
from shared.data import get_session, create_tables
from shared.data.defs import *

session = get_session() # för default-databasen
session = get_session("sqlite:///tester/db/haxlol.db")
create_tables() # skapar tables som inte finns i db:n

print session.bind
print session.query(Unit).all()
print session.add(Unit(u"lolbollarN^"))
print session.query(Unit).all()
session.commit() # för att trycka in det i databasen


