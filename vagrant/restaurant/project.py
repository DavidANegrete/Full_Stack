from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from restaurant_methods import *
app = Flask(__name__)

#New IMPORTS OF FOR OATH:
from flask import session as login_session
  #Will use this to create a psuedo random string
import random, string

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Creating a state token to preven request forgery
#Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return "The current sessions state is %s " %login_session['state']



@app.route('/restaurants/')
def retaurantIndex():
    allRestaurants = getRestaurants()
    return render_template('restaurants.html', allRestaurants=allRestaurants )



@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'], 
            price=request.form['price'], 
            course=request.form['course'], 
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Item Created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newItem.html', restaurant_id=restaurant_id, restaurant=restaurant)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    if request.method == 'POST':
        if request.form['name']:
            editMenu.name = request.form['name']
        if request.form['description']:
            editMenu.description = request.form['description']
        if request.form['price']:
            editMenu.price= request.form['price']
        if request.form['course']:
            editMenu.course= request.form['course']
        session.add(editMenu)
        session.commit()
        flash("Item modified")
        return redirect(url_for('restaurantMenu', restaurant =restaurant, restaurant_id=restaurant_id,items=items))
    else:
        return render_template('editMenu.html', restaurant_id=restaurant_id, menu_id=menu_id, menuItem=editMenu,restaurant=restaurant)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)

#API Endpoint (GET Requests)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=[item.serialize])


    


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)