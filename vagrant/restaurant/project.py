from flask import Flask, render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

# Creates a stagging area to add to the db
session = DBSession()

#home
@app.route('/')
@app.route('/restaurants.in/')
def home():
    '''This method renders the home template'''
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(id = restaurant.id)
    return render_template('menu.html', items=items, restaurant=restaurant)

@app.route('/restaurants.in/<int:menu_id>/<int:restaurant_id>/edit', methods=['POST', 'GET'])
def editMenuItem(menu_id, restaurant_id):
    '''This method renders the home template'''
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).first()

    return render_template('edit.html', item=item, restaurant_id=restaurant_id)

@app.route('/restaurants.in/<int:menu_id>/<int:restaurant_id>/delete', methods=['POST', 'GET'])
def deleteMenuItem(menu_id, restaurant_id):
    '''This method renders the home template'''

    return render_template('delete.html', menu_id=menu_id, restaurant_id=restaurant_id)

@app.route('/restaurants.in/<int:restaurant_id>/new', methods=['POST', 'GET'])
def newMenuItem(restaurant_id):
    '''This method renders the home template'''

    return render_template('new_item.html', restaurant_id=restaurant_id)
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
