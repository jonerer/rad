# -*- coding: utf-8 -*

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, \
        Float, Unicode, Boolean, DateTime
from sqlalchemy.orm import relation, backref

Base = declarative_base()

# lägg allt som ska synas utåt här: (dessa får man från from shared.data.defs import *
__all__ = ['UnitType', 'Unit', 'User', 'Mission', 'Document', 'AlarmType', 'Alarm', 'Poi']

class UnitType(Base):
    __tablename__ = "unit_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    image = Column(String)

    def __init__(self, name, image):
        self.name = name
        self.image = image

class AlarmType(Base):
    __tablename__ = "alarm_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    image = Column(String)

    def __init__(self, name, image):
        self.name = name
        self.image = image

class POIType(Base):
    __tablename__ = "poi_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    image = Column(String)

    def __init__(self, name, image):
        self.name = name
        self.image = image

class Poi(Base):
    __tablename__ = "poi"
    coordx = Column(Float)
    coordy = Column(Float)
    db_id = Column(Integer, primary_key=True)
    id = Column(Integer)
    name = Column(Unicode)
    sub_type = Column(Unicode) 
    timestamp = Column(DateTime)
    type_id = Column(Integer, ForeignKey("poi_types.id"))
    type = relation(POIType, backref=backref("pois", order_by=id)) 

class Alarm(Base):
    __tablename__ = "alarm"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    type_id = Column(Integer, ForeignKey("alarm_types.id"))
    type = relation(AlarmType, backref=backref("alarm", order_by=id))
    extrainfo = Column(Unicode)
    coordx = Column(Float)
    coordy = Column(Float)
    timestamp = Column(DateTime)


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    coordx = Column(Float) # longitude
    coordy = Column(Float) # latitude
    type_id = Column(Integer, ForeignKey("unit_types.id"))
    type = relation(UnitType, backref=backref("units", order_by=id))
    is_self = Column(Boolean)

    def get_image(self):
        if not self.is_self:
            return type.image
        else:
            return "JonasInGlases.png"

    def __init__(self, name, type, coordx=None, coordy=None, is_self=False):
        self.name = name
        self.type = type
        self.coordx = coordx
        self.coordy = coordy
        self.is_self = is_self
        
    def __repr__(self):
        return "Unit '%s' of type %s" % (self.name, self.type)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    password = Column(Unicode)

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
#Jonas Leker
#SKA HA EN USER
class Mission(Base):
    __tablename__ = "mission"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    coordx = Column(Float)
    coordy = Column(Float)
    info = Column(Unicode)
    prio = Column(Integer)
    
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.id, self.name)
    
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    ownerId = Column(Integer)
    path = Column(String)
    
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.name, self.type)    

