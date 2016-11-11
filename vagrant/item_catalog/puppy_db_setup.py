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
    picture = Column(String(250))

class Pet(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    
    animal_type = Column(String(80), nullable = False)
    breed = Column(String(80), nullable = False)
    color = Column(String(80), nullable = False)
    gender = Column(String(8))
    zipCode = Column(String(8))

    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'animal_type': self.animal_type,
        'breed': self.breed,
        'zipCode': self.zipCode}

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    is_lost = Column(String(250), nullable=False)
    is_found = Column(String(6), nullable = False)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    entered_by = Column(Integer, ForeignKey('user.id'))
    shelter = relationship(Shelter)
    user = relationship(User)
    weight = Column(Integer)
    adopted = Column(Boolean, nullable=False, default=False)

    @property
    def serialize(self):
        return {'id': self.id,'name': self.name,'gender': self.gender,}

# A one to many table to show the relationship between an users and pups
class UserAndPuppy(Base):
    __tablename__ = 'user_and_puppy'
    userId = Column(Integer, ForeignKey(User.id), primary_key = True)
    puppyId = Column(Integer, ForeignKey(Puppy.id), primary_key = True)
    puppy = relationship(Puppy)
    user = relationship(User)

# Table to track new families
class NewFamily(Base):
    __tablename__ = 'new_family'
    id = Column(Integer, primary_key=True)
    adopter_id = Column(Integer, ForeignKey('user.id'))
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    adopter_name = Column(String(250), nullable=False)
    puppy_name = Column(String(250), nullable=False)
    shelter = relationship(Shelter)
    puppy = relationship(Puppy)
    user = relationship(User)

engine = create_engine('sqlite:///puppyshelterwithusers.db')

Base.metadata.create_all(engine)
