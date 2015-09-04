#this script will fill the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#specifies what db will be used

#Section in
#specifies what db will be used
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

#creates a stagging area to add to the db
session = DBSession()


#Created session object to not have to rewrite always 
queryRestaurant = session.query(Restaurant)
queryMenuItem = session.query(MenuItem)

#method to get all restaurants
def getRestaurants():
	return queryRestaurant.all()

#method to set a restaurant
def setRestaurant(name):
	restaurant = Restaurant(name=name)
	session.add(restaurant)
	session.commit()
	print name + " has been added to the restaurant DB!"


#bucks  = Restaurant(name = "Chucks")
#session.add(bucks)
#session.commit()
#cheesepizza = MenuItem(name= "Cheese Pizza", description = "Made with meat", course = "Entree", price="10.00", restaurant = bucks)
#session.add(cheesepizza)
#session.commit()

#print session.query(Restaurant).all()



