# -*- coding: utf-8 -*

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, \
        Float, Unicode, Boolean, DateTime
from sqlalchemy.orm import relation, backref


Base = declarative_base()

# lägg allt som ska synas utåt här: (dessa får man från from shared.data.defs import *
__all__ = ['UnitType', 'Unit', 'User', 'Mission', 'Document', 'POI', 'POIType']

class UnitType(Base):
    __tablename__ = "unit_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    image = Column(String)

    def __init__(self, name, image):
        self.name = name
        self.image = image

#class AlarmType(Base):
    #__tablename__ = "alarm_types"
    #id = Column(Integer, primary_key=True)
    #name = Column(Unicode)
    #image = Column(String)

    #def __init__(self, name, image):
        #self.name = name
        #self.image = image

class POIType(Base):
    __tablename__ = "poi_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    image = Column(String)

    def __init__(self, name, image):
        self.name = name
        self.image = image

class POI(Base):
    __tablename__ = "poi"
    coordx = Column(Float)
    coordy = Column(Float)
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    time_created = Column(Integer)
    time_changed = Column(Integer)
    type = relation(POIType, backref=backref("poi", order_by=id)) 
    subtype = Column(Unicode) 
    
    uid = Column(Integer) #Internt ID?
    type_id = Column(Integer, ForeignKey("poi_types.id"))
    
    
    def __init__(self, coordx, coordy, uid, name, type, subtype, time_created, time_changed):
        from shared.data import get_session, create_tables
        session = get_session()
        self.coordx = coordx
        self.coordy = coordy
        self.uid = uid
        self.type = type
        self.subtype = subtype
        self.name = name
        self.time_created = time_created
        self.time_changed = time_changed
        
#class Alarm(Base):
    #__tablename__ = "alarm"
    #id = Column(Integer, primary_key=True)
    #name = Column(Unicode)
    #type_id = Column(Integer, ForeignKey("alarm_types.id"))
    #type = relation(AlarmType, backref=backref("alarm", order_by=id))
    #extrainfo = Column(Unicode)
    #coordx = Column(Float)
    #coordy = Column(Float)
    #timestamp = Column(DateTime)

    #def __init__(self, coordx, coordy, id, name, sub_type, timestamp):
        #self.coordx = coordx
        #self.coordy = coordy
        #self.id = id
        #self.name = name
        #self.sub_type = sub_type
        #self.timestamp = timestamp


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    coordx = Column(Float) # longitude
    coordy = Column(Float) # latitude
    type = relation(UnitType, backref=backref("units", order_by=id))
    time_changed = Column(Integer)
    
    is_self = Column(Boolean)
    type_id = Column(Integer, ForeignKey("unit_types.id"))

    def get_image(self):
        if not self.is_self:
            return type.image
        else:
            return "JonasInGlases.png"

    def __init__(self, name, type, coordx, coordy, time_changed, is_self):
        self.name = name
        self.type = type
        self.coordx = coordx
        self.coordy = coordy
        self.time_changed = time_changed
        self.is_self = is_self
        
    def __repr__(self):
        return "Unit '%s' of type %s" % (self.name, self.type)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    password = Column(Unicode)
    type_id = Column(Integer, ForeignKey("units.id"))
    type = relation(Unit, backref=backref("users", order_by=id))

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
#Jonas Leker
#SKA HA EN USER
class Mission(Base):
    __tablename__ = "mission"
    id = Column(Integer, primary_key=True)
    time_created = Column(Integer)
    time_changed = Column(Integer)
    name = Column(Unicode)
    coordx = Column(Float)
    coordy = Column(Float)
    status = Column(Unicode)
    desc = Column(Unicode)
    
    # poi_ids = ?? RELATION ??
    # unit_ids = ?
    
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
