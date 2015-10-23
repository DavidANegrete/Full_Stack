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

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    max_capacity = Column(Integer)
    current_capacity = Column(Integer)

    @property
    def serialize(self):
        return {'id': self.id,'name': self.name,}

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
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
