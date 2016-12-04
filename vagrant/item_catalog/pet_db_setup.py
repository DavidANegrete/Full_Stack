import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=True)

class Pet(Base):
    ''' Represents a pet that is either lost or found'''
    __tablename__ = 'pet'
    id = Column(Integer, primary_key = True)
    animal_type = Column(String(80), nullable = False)
    description = Column(String(250), nullable = True)
    breed = Column(String(80), nullable = True)
    gender = Column(String(8))
    name = Column(String(80), nullable = True)
    picture = Column(String(250), nullable = False)
    zipcode = Column(String(8), nullable = False)

    @property
    def serialize(self):
        return {
        'id': self.id,
        'animal_type': self.animal_type,
        'breed': self.breed,
        'name': self.name,
        'zipCode': self.zipCode}

class Status(Base):
    ''' This class represents a pets given status as either
    lost found or on_the_run. Their are two foreign key relationships 
    one between pet.id and the other user.id.'''
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    is_lost = Column(Boolean, unique=False, default=False)
    is_found = Column(Boolean, unique=False, default=False)
    on_the_run = Column(Boolean, unique=False, default=False)
    pet_id = Column(Integer, ForeignKey('pet.id'))
    entered_by = Column(Integer, ForeignKey('user.id'))
    pet = relationship(Pet)
    user = relationship(User)

    @property
    def serialize(self):
        return {
        'id': self.id,
        'is_lost': self.is_lost,
        'is_found': self.is_found,
        'is_on_the_run': self.is_on_the_run,
        'pet_id': self.pet_id
        }


engine = create_engine('sqlite:///lostandfoundpets.db')

Base.metadata.create_all(engine)
