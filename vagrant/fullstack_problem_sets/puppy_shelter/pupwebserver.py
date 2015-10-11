from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
app = Flask(__name__)

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker  
from puppy_db_setup import Base, Shelter, Puppy, User, UserAndPuppy

import random, string
from pup_methods import * 

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

import logging

#getting the client id to cross check authentication
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Pups in the City"

engine = create_engine('sqlite:///puppyshelterwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#global variables
pupQuery = session.query(Puppy)

shelterQuery = session.query(Shelter)

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    #see if connected
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id




    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Auth code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
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

    # Store the access session token
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECTING  - Revoking the current user's token and reset the login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
   
@app.route('/')
@app.route('/pups/')
def pups():
	return render_template('pupshome.html')

#search for a pup  
@app.route('/pups/search/', methods=['GET', 'POST'])
def pupsSearch():
    
    if request.method == 'POST':

    	startDate= ''
    	endDate= ''  
    	ageRange = {}
        kwargs = { x:request.form[x] for x in request.form if request.form[x] and request.form[x] != 'default' }
        
        #Method from pup_meth getAgeRange(var): take a numeric variable and returns a coresponding age range in the form of a dictionay. 
        ageRange=getAgeRange(kwargs['dateOfBirth'])
        
        #startDate is the closest to the current date on any search.
        for key in ageRange:
        	endDate = key
        	startDate = ageRange[key]
		
		#puppy_list is a query object with all the puppies in the db. 
		puppy_list = session.query(Puppy, Shelter).filter(Puppy.shelter_id == Shelter.id)
		holder = kwargs['name']
		#Checking if the value from input='name' is the same or less than 3 and return the puppy_list 
		# or the search continues
		if len(holder) >= 3 and holder == 'Name':
			puppy_list=puppy_list
		else:
			name = kwargs['name'].strip().title()
			if name:
				    puppy_list = puppy_list.filter(Puppy.name == name)

        #block to check the gender selected	
        if kwargs['gender'] == 'either':
        	puppy_list = puppy_list
        else:
        	if kwargs['gender'] == 'female':
        		puppy_list = puppy_list.filter(Puppy.gender == 'female')
        	else:
        		puppy_list = puppy_list.filter(Puppy.gender == 'male')

        #start and end are called at the start of the block and use a method from pup_meth to get the range.
        if kwargs['dateOfBirth'] == 'any':
        	puppy_list = puppy_list
        else:
        	puppy_list = puppy_list.filter(and_(Puppy.dateOfBirth <= startDate, Puppy.dateOfBirth >= endDate))
        
        #block of code used to pick the shelter from the shelters in the db
        if kwargs['shelter_id'] == 'all':
        	puppy_list = puppy_list
        else:
        	sh_id = kwargs['shelter_id']
        	puppy_list = puppy_list.filter(Puppy.shelter_id == Shelter.id).filter(Puppy.shelter_id == int(sh_id)).all()
        # rendering new page with results.
        return render_template('searchresults.html', puppy_list=puppy_list)

    # N.b. I moved this statement as it is only useful for GET requests:
    shelters = session.query(Shelter)
    return render_template('pupssearch.html', shelters=shelters)
	
@app.route('/pups/adopt/<int:pup_id>/<int:shelter_id>', methods=['GET', 'POST'])
def pupsAdopt(pup_id, shelter_id):
    
    #checking to see if the user is logged in
    if 'username' not in login_session:
        return redirect ('/login')
	  
    if request.method == 'POST':
        return  render_template('pupsnewparent.html')


	pup = session.query(Puppy).filter(Puppy.id==pup_id, shelter_id==shelter_id).one()
	shelter = session.query(Shelter).filter(Shelter.id==shelter_id).one()
	return render_template('pupsadopt.html',pup=pup, shelter=shelter)

@app.route('/pups/rehome/', methods=['GET', 'POST'])
def pupsRehome():
    #checking to see if the user is logged in
    if 'username' not in login_session:
        return redirect ('/login')

    #get dictionary for vacant shelters. 
    vac_shelters = vacantShelter()

    if request.method == 'POST':
        kwargs = { x:request.form[x] for x in request.form if request.form[x] and request.form[x] != 'default' }
        name = kwargs['name']
        gender = kwargs['gender']
        dateOfBirth= kwargs['dateOfBirth']
        picture = 'http://www.graphicsdb.com/data/media/441/human_dog_face.jpg'
        weight = kwargs['weight']
        shelter_id = kwargs['shelter']
        entered_by=login_session['user_id']


        #addPup(name, gender, dateOfBirth, picture, weight, shelter_id, entered_by)
        addPup(name, gender, dateOfBirth, picture, weight, shelter_id, entered_by)
        print entered_by
        flash(name + ' has been added to the DB')

        return render_template('pupshome.html')






    return render_template('pupsrehome.html', shelters=vac_shelters)

@app.route('/pups/edit/<int:pup_id>/', methods=['GET', 'POST'])
def pupsEdit(pup_id):
    #checking to see if the user is logged in

	return render_template('pupsedit.html')

@app.route('/pups/delete/<int:pup_id>/', methods=['GET', 'POST'])
def pupsDelete(pup_id):
    #checking to see if the user is logged in

	return render_template('pupsdelete.html')





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)