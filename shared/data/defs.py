# -*- coding: utf-8 -*

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, Unicode
from sqlalchemy.orm import relation, backref

Base = declarative_base()

# lägg allt som ska synas utåt här: (dessa får man från from shared.data.defs import *
__all__ = ['UnitType', 'Unit', 'User', 'Mission', 'Document']

class UnitType(Base):
    __tablename__ = "unit_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    image = Column(String)

    def __init__(self, name, image):
        self.name = name
        self.image = image

class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    coordx = Column(Float) # longitude
    coordy = Column(Float) # latitude
    type_id = Column(Integer, ForeignKey("unit_types.id"))
    type = relation(UnitType, backref=backref("units", order_by=id))

    def __init__(self, name):
        self.name = name
        
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

