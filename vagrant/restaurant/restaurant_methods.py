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

#method to get the first restuarant
def getFirstRestaurant():
	return session.query(Restaurant).first()

def getRestaurantMenuItems(restaurant_id):
	return queryRestaurant.filter(MenuItem.restaurant_id==restaurant_id).all()


#method to set a restaurant
def setRestaurant(name):
	restaurant = Restaurant(name=name)
	session.add(restaurant)
	session.commit()
	print name + " has been added to the restaurant DB!"

#method to add a restaurant menu item, takes 5 attributes 
#restaurant_id: FK (Restaurant)

def setRestaurantMenuItem(restaurant_id, name, description, price, course):
	item = MenuItem(name=name,description=description,price=price,course=course,restaurant_id=restaurant_id)
	session.add(item)
	session.commit()
	print 'Item Added'
