from flask import Flask, render_template, request, redirect, url_for, flash, jsonify


from database_setup import Base, Restaurant, MenuItem, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets #JSON formated file. It stores the OAUTH2 parameters
from oauth2client.client import FlowExchangeError #Used to catch errors
import httplib2 #Comprehensive HTTP library in Python
import json #Used for converting in memory Python objects to a syreializxed 
            # representation, known as JSON, or Java Script Object Notation 
from flask import make_response #converts the return value from a function into a real response object 
import requests #Apache 2.0 licensed HTTP library written in Python like urlib

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)


@app.route('/gconnect', methods = ['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the ' +
        'authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])
    # If there is an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style = "width: 300px; height: 300px;border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Disconnect a logged in user by revoking his token and resetting his login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('credentials')
    if access_token is None:
        # in this case no user has been logged in
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # revoke the token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the users session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # the given token is invalid
        response = make_response(json.dumps('Failed to revoke token'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"

    # strip expire tag from access token
    token = result.split("&")[0]
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, 
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash('You are now signed in!')

    return render_template('pupshome.html')
# User Helper Functions
def createUser(login_session):
    ''' This method takes in a login_session as input, then creates a new user
    in the database and extracts all the fields neessary to pupulate it with the 
    information gathered from the login_session, finally it returns the user ID 
    of the new user created'''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    ''' This method takes a user_id and returns a user object associated with 
    this ID number'''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    ''' This method takes an email and returns the User ID that belongs to that email,
    if not found returns none'''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/restaurants.in/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants.in/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])



@app.route('/')
@app.route('/restaurants.in/')
def home():
    '''This method renders either a public template or a private one and 
    passes the a user object that created if it is privaterestaurants to
    the user or the signed in-template'''
    restaurants = session.query(Restaurant)
    if 'username' not in login_session:
        return render_template('public_restaurants.html', restaurants=restaurants)
    else:
        creator = getUserInfo(getUserID(login_session['email']))
        return render_template('restaurants.html', restaurants=restaurants, creator= creator)

@app.route('/restaurants.in/new/', methods=['POST', 'GET'])
def newRestaurant():
    '''This method renders the home template'''
    if 'username' not in login_session:
        return redirect('/login')
    restaurants = session.query(Restaurant)
    if request.method == 'POST':
        restaurant = Restaurant(name = request.form['name'],
            user_id = login_session['user_id'])
        session.add(restaurant)
        session.commit()
        flash('A new restaurant was added!')
        return redirect(url_for('home', restaurants = restaurants))
    return render_template('newRestaurant.html', )

@app.route('/restaurants.in/<int:restaurant_id>/edit/', methods=['POST', 'GET'])
def editRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurants = session.query(Restaurant)
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('A restaurant name was changed')
        return redirect(url_for('home', restaurants = restaurants))
    return render_template('edit_restaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)

@app.route('/restaurant.in/<int:restaurant_id>/delete/', methods=['POST', 'GET'])
def deleteRestaurant(restaurant_id):
    ''' This method takes a restaurant_id and will delete that restaurant, if 
    the user is logged in and the person that created it or it will redirect
    the user and give an error message'''
    if 'username' not in login_session:
        return redirect('/login')    
    restaurants = session.query(Restaurant)
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized\
            to delete this restaurant. Please create your own restaurant in \
            order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if restaurant.name == request.form['name']:
            session.delete(restaurant)
            session.commit
            flash(restaurant.name + ' has been removed!')
        return redirect(url_for('home', restaurants = restaurants))
    return render_template('delete_restaurant.html', restaurant=restaurant)

@app.route('/restaurants.in/<int:restaurant_id>/')
@app.route('/restaurants.in/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    ''' This method takes a restaurant_id and returns two different templates.
    If a user isn't logged in or the original creator a public template is displayed 
    or a private template is displayed'''
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template(
            'public_menu.html', 
            items=items, 
            restaurant=restaurant, 
            creator=creator)
    else:
        return render_template(
            'restaurant_menu.html', 
            items = items, 
            restaurant=restaurant, 
            creator =creator)

@app.route('/restaurants.in/<int:restaurant_id>/new/', methods=['POST', 'GET'])
def newMenuItem(restaurant_id):
    '''
    This menthod checks to see if a post request is recieved and redirects a user.'''
    if 'username' not in login_session:
        return redirect('/login')    
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    items = session.query(MenuItem).filter_by(id = restaurant.id)
    if request.method == 'POST':
    	item = MenuItem(
    		name = request.form['name'],
    		description = request.form['description'], 
    		course = request.form['course'],
    		price = request.form['price'],  
    		restaurant_id = restaurant_id, 
            user_id=restaurant.user_id)
    	session.add(item)
    	session.commit()
        flash("New item added for " + restaurant.name)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
    else:
        return render_template('new_item.html', restaurant_id=restaurant_id, restaurant = restaurant)

@app.route('/restaurants.in/<int:menu_id>/<int:restaurant_id>/edit/', methods=['POST', 'GET'])
def editMenuItem(menu_id, restaurant_id):
    '''This method renders the home template'''
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name'] != item.name:
            item.name = request.form['name']
        if request.form['course'] != item.course:
            item.course = request.form['course']
        if request.form['price'] != item.price:
            item.price = request.form['price']
        if request.form['description'] != item.description:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash("An item has been modified for " + restaurant.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    return render_template('edit.html', item=item, restaurant_id=restaurant_id)

@app.route('/restaurants.in/<int:menu_id>/delete/', methods=['POST', 'GET'])
def deleteMenuItem(menu_id):
    '''This method renders the home template'''
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = item.restaurant_id)
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("A menu item has been removed " )
        return redirect(url_for('restaurantMenu', restaurant_id = item.restaurant_id))
    return render_template('delete_item.html', menu_id=menu_id, item=item)
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
