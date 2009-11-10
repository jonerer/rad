# -*- coding: utf-8 -*

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, Unicode
from sqlalchemy.orm import relation, backref

Base = declarative_base()

class EntityType(Base):
    __tablename__ = "entity_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    image = Column(String)

class Entity(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    password = Column(Unicode)
    longitude = Column(Float)
    latitude = Column(Float)
    type_id = Column(Integer, ForeignKey("entity_types.id"))
    type = relation(EntityType, backref=backref("entities", order_by=id))

    def __init__(self, name, password):
        self.name = name
        self.password = password
        
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.name, self.password)
    
#Jonas Leker
#Vet inte riktigt skillnaden på Unicode och String, kan vara så att
#vi inte behöver ha unicode på info!!!
#SKA HA EN USER
class Mission(Base):
    __tablename__ = "mission"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    longitude = Column(Float)
    latitude = Column(Float)
    info = Column(Unicode)
    prio = Column(Integer)
    
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.id, self.name)
    
class Documents(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    ownerId = Column(Integer)
    path = Column(String)
    
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.name, self.type)    

