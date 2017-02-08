import sys
from sqlalchemy import (Column, ForeignKey, Integer, 
                        String, Date, Numeric, Boolean, Enum)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key=True)

class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer,ForeignKey('user.id'))
	user = relationship(User)

class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(Enum('breakfast', 'lunch', 'dinner'), nullable = False)
	description = Column(String(250), nullable = False)
	price = Column(String(8), nullable = False)
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.create_all(engine)
