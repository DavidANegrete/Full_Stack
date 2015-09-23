#
#This file creates a database using SQLAlchemy
#There are 4 steps to using it 
#1. Configuration - imports all the modules
#   - at the begining of the file 
#   - imports all modules needed
#   - creates the declarative base
#   - at the end of the configuration file it creates the database and adds tables and colums
#2. class - used to represent the data in python
#3. table - represent the table in the db
#4. mapper - reps the class the represents the columns with the class that represents the data

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

class MenuItem(Base):
	__tablename__ = 'menu_item'
	
	id = Column(Integer, primary_key = True)
	name =Column(String(80), nullable = False)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property 
	def serialize(self):
		#returns data in a serialized format
		return {
		'name' : self.name,
		'description' : self.description,
		'id' : self.id,
		'price': self.price,
		'course' : self.course
		}



engine = create_engine('sqlite:///restaurantmenu.db') 

Base.metadata.create_all(engine)




