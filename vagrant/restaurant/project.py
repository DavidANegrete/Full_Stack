from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/', methods=['GET','POST'])
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('create.html', restaurant=restaurant)


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/create')
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	return render_template('create.html', restaurant=restaurant)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>')
def editMenuItem(restaurant_id, menu_id):
	#get restaurant from the id
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)