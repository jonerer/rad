from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float
from sqlalchemy.orm import relation, backref

Base = declarative_base()

print __all__
__all__ = ['EntityType', 'Entity']
class EntityType(Base):
    __tablename__ = "entity_types"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, length=255)
    image = Column(String, length=255)

class Entity(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, length=255)
    longitude = Column(Float)
    latitude = Column(Float)
    type_id = Column(Integer, ForeignKey("entity_types.id"))

    type = relation(EntityType, backref=backref("entities", order_by=id))

    def __repr__(self):
        return "Entity '%s' of type %s" % (self.name, self.type)
    
#Jonas Leker
#Vet inte riktigt skillnaden på Unicode och String, kan vara så att
#vi inte behöver ha unicode på info!!!
class Mission(Base):
    __tablename__ = "mission"
    id = column(Integer, primary_key=True)
    name = column(Unicode, length=255)
    longitude = column(Float)
    latitude = column(Float)
    info = column(Unicode, length=255)
    prio = column(Integer)
    
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.name, self.type)
    
class Documents(Base):
    __tablename__ = "documents"
    id = column(Integer, primary_key=True)
    name = column(Unicode, length=255)
    ownerId = column(Integer)
    path = column(String, length=255)
    
    def __repr__(self):
        return "Entity '%s' of type %s" % (self.name, self.type)    
    

