from flask import Flask, render_template, request, redirect 
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy,User 
from puppy_db_setup import UserAndPuppy, User, NewFamily
from flask import session as login_session
from werkzeug import secure_filename
from functools import wraps
import os
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from pup_methods import *
import logging

# Constants for uploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

# setting up the upload folder for the images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cross check Authentication
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Pups in the City"

# Connect to the Database and session
engine = create_engine('sqlite:///puppyshelterwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Session variables for querys
pupQuery = session.query(Puppy)
shelterQuery = session.query(Shelter)
userQuery = session.query(User)
queryPupnShelter = session.query(Puppy, Shelter)

# Decorator function to keep views accisible by some only.
def logInDecorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if 'username' not in login_session:
            return redirect (url_for('showLogin', next = request.url))
        return f(*args, **kwds)
    return wrapper


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE = state)


# FB - loggin
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


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    fb_permission_url = 'https://graph.facebook.com/%s/permissions?access_token=%s'
    url = fb_permission_url% (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
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
        response = make_response(json.dumps('User is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    # Data variable passes data to the login session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    # Chek if user exists, if not makes a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash('You are nog logged in!')
    return render_template('pupshome.html')

# Creates a new user if called and returns the new users id
def createUser(login_session):
    newUser = User(name = login_session['username'],
                    email = login_session['email'],
                    picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = userQuery.filter_by(email=login_session['email']).one()
    return user.id

# Gets the user info from the user ID
def getUserInfo(user_id):
    user = userQuery.filter_by(id=user_id).one()
    return user

# Gets the user ID from the email on the login session
def getUserID(email):
    try:
        user = userQuery.filter_by(email=email).one()
        return user.id
    except:
        return None

# Disconnect
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('pups', control_notice='true'))
    else:
        flash("You were not logged in")
        return redirect(url_for('pups',control_notice=notice, error='true'))

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
    access_token = login_session['credentials']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON requests
# JSON APIs returns pups in each shelter based on certain querries
@app.route('/pups/<int:shelter_id>/shelter/JSON')
def pupsInShelterJSON(shelter_id):
    shelter = session.query(Puppy).filter_by(shelter_id=shelter_id).all()
    by_shelter = session.query(Puppy).filter_by(shelter_id=shelter_id).all()
    return jsonify(Puppy=[i.serialize for i in by_shelter])

@app.route('/')
@app.route('/pups/')
def pups():
    return render_template('pupshome.html')

# Search for a pup  
@app.route('/pups/search/', methods=['GET', 'POST'])
def pupsSearch():
    if request.method == 'POST':
        startDate= ''
        endDate= ''  
        ageRange = {}
        kwargs = { x:request.form[x] for x in request.form 
        if request.form[x] and request.form[x] != 'default' }
        
        # Method from pup_meth getAgeRange(var): take a numeric 
        # variable and returns a coresponding age range in the form of a dict. 
        ageRange=getAgeRange(kwargs['dateOfBirth'])
        
        # StartDate is the closest to the current date on any search.
        for key in ageRange:
            endDate = key
            startDate = ageRange[key]
        
        # puppy_list is a query object with all the puppies in the db. 
        puppy_list = session.query(Puppy, Shelter).filter(
            Puppy.shelter_id == Shelter.id)
        holder = kwargs['name']

        # Checking if the value from input='name' is the same or less 
        # than 3 and return the puppy_list or the search continues
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

        # start and end are called at the start of the block and use
        # a method from pup_meth to get the range.
        if kwargs['dateOfBirth'] == 'any':
            puppy_list = puppy_list
        else:
            puppy_list = puppy_list.filter(and_(Puppy.dateOfBirth <= startDate,
            Puppy.dateOfBirth >= endDate))
        
        # Block of code used to pick the shelter from the shelters in the db
        if kwargs['shelter_id'] == 'all':
            puppy_list = puppy_list
        else:
            sh_id = kwargs['shelter_id']
            puppy_list = puppy_list.filter(Puppy.shelter_id == Shelter.id)
            puppy_list = puppy_list.filter(Puppy.shelter_id == int(sh_id)).all()
 
        # If they are logged in they can see the pups available and 
        # get an option to adopt if not only the pups will show.
        if 'username' not in login_session:
            return render_template(
            'signedoutresults.html', puppy_list=puppy_list)
        else:
            # rendering view with the option to adopt and edit/delete if a user
            # is the same as the one that enered the pup
            user_id=getUserID(login_session['email'])
            return render_template(
            'searchresults.html', puppy_list=puppy_list, user_id=user_id)
    shelters = session.query(Shelter)
    return render_template('pupssearch.html', shelters=shelters)
	
@app.route('/pups/adopt/<int:pup_id>', methods=['GET', 'POST'])
@logInDecorator
def pupsAdopt(pup_id): 
    pup = session.query(Puppy).filter_by(id=pup_id).one()
    shelter =session.query(Shelter).filter_by(id=pup.shelter_id).one()
    if request.method == 'POST':
        adopter_id = getUserID(login_session['email'])
        puppy_id = pup.id
        shelter_id = pup.shelter_id
        adopter_name = login_session['username']
        puppy_name = pup.name
        newfam = NewFamily(adopter_id = adopter_id, puppy_id = puppy_id,
                            shelter_id = shelter_id,adopter_name = adopter_name,
                            puppy_name = puppy_name)
        session.add(newfam)
        session.commit()

        session.delete(pup)
        session.commit()            
        flash('You have adopted this pup!')
        # Method to delete a pup removes him
        
        return render_template('pupshome.html')
    return render_template('pupsadopt.html', pup=pup, shelter=shelter)



# making sure that the files uploaded are images only
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# This method returns a URL of an uploaded file
def show(file):
    filename = 'http://127.0.0.1:5000/static/images/uploads/' + file
    return filename


@app.route('/pups/rehome/', methods=['GET', 'POST'])
@logInDecorator
def pupsRehome():
    # get dictionary for any shelters with space available.
    vac_shelters = vacantShelter()

    if request.method == 'POST':
        kwargs = { x:request.form[x] for x in request.form 
        if request.form[x] and request.form[x] != 'default' }

        name = kwargs['name']
        gender = kwargs['gender']
        dateOfBirth = kwargs['dateOfBirth']
        file = request.files['file']
        if not file:
            picture = '/static/images/no-image.jpg'
        weight = kwargs['weight']
        shelter_id = kwargs['shelter']
        entered_by=getUserID(login_session['email'])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            picture = show(filename)
        print picture



        # this method was comes from pup_methods
        # It takes in 7 variables and adds a new pup in the DB
        addPup(name, gender, dateOfBirth, picture,
                    weight, shelter_id, entered_by)
        # setting notice to display flash messag
        control_notice = 'true'
        flash( name + ' has been added hopefully he gets adopted soon.')
        return render_template('pupshome.html')

    return render_template('pupsrehome.html', shelters=vac_shelters)

@app.route('/pups/edit/<int:pup_id>/', methods=['GET', 'POST'])
@logInDecorator
def pupsEdit(pup_id):
    pupToEdit = pupQuery.filter_by(id=pup_id).one()

    # throwing and error and redirecting if not authorized to change the pup
    if pupToEdit.entered_by != login_session['user_id']:
        flash('Not authorized to change a pup you did not enter in the system.')
        return render_template('pupshome.html', error = 'true')
    current_shelter = shelterQuery.filter_by(id=pupToEdit.shelter_id).one()
   
    # get any shelters with space available from vacantShelter. 
    vac_shelters = vacantShelter()
    
    if request.method == 'POST':
        if request.form['name'] != pupToEdit.name:
            name = request.form['name']
            if name:
                pupToEdit.name = name
        if request.form['gender'] != pupToEdit.gender:
            gender = request.form['gender']
            if gender:
                pupToEdit.gender = gender
        if request.form['dateOfBirth'] != pupToEdit.dateOfBirth:
            # getDOB converts a string into a date object
            dob = getDOB(request.form['dateOfBirth'])
            if dob:
                pupToEdit.dateOfBirth = dob
        
        # Checking if a different image was selected.
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add the removal of the file from the server
            
        if request.form['weight'] != pupToEdit.weight:
            weight = request.form['weight']
            if weight:
                pupToEdit.weight = weight
        if request.form['shelter'] != pupToEdit.shelter_id:
            shelter_id = request.form['shelter']
            if shelter_id:
                new_shelter = shelterQuery.filter_by(id=shelter_id).one()
                pupToEdit.shelter_id = shelter_id
        flash('Changes made!')
        session.add(pupToEdit)
        session.commit()
        return render_template('pupshome.html', notice='true')
    return render_template('pupsedit.html', pup_id = pup_id, pup = pupToEdit,
        vac_shelters=vac_shelters, current_shelter = current_shelter)

@app.route('/pups/delete/<int:pup_id>/', methods=['GET', 'POST'])
@logInDecorator
def pupsDelete(pup_id):
    pupToDelete = session.query(Puppy).filter_by(id=pup_id).one()

    #throwing and error and redirecting if not authorized to change the pup
    if pupToDelete.entered_by != getUserID(login_session['email']):
        flash('Not authorized to delete a pup you did not enter in the system.')
        return render_template('pupshome.html')

    # checking to see if the creator is the deleter
    if getUserID(login_session['email']) == pupToDelete.entered_by:
        if request.method == 'POST':
            if pupToDelete.name.lower() == request.form['name'].strip().lower(): 
                session.delete(pupToDelete)
                session.commit()            
                flash( 'Pup has been removed')
                return render_template('pupshome.html')
            else:
                flash( "Enter the exact spelling of the name!")
                return render_template('pupsDelete.html', pup_id=pup_id)
    return render_template('pupsdelete.html', pup_id = pup_id, puppy = pupToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
