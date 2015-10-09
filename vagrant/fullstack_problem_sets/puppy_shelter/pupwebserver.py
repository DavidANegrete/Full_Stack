from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker  
from puppy_db_setup import Base, Shelter, Puppy, Adoptor, AdoptorAndPuppy
from pup_meth import * 
import logging
# Create session and connect to DB


# Create session and connect to DB
app = Flask(__name__)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#global variables
pupQuery = session.query(Puppy)

shelterQuery = session.query(Shelter)

@app.route('/pups/login/')
def login():
	return render_template('login.html')


@app.route('/')
@app.route('/pups/')
def pups():
	return render_template('pupshome.html')
@app.route('/pups/test')
def pupsTest():
	return render_template('pupttest.html')


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
        #block of code used to pick the shelter from the shelters in the the db
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
	if request.method == 'POST':

		return  render_template('pupsnewparent.html')


	pup = session.query(Puppy).filter(Puppy.id==pup_id, shelter_id==shelter_id).one()
	shelter = session.query(Shelter).filter(Shelter.id==shelter_id).one()
	return render_template('pupsadopt.html',pup=pup, shelter=shelter)

@app.route('/pups/rehome/', methods=['GET', 'POST'])
def pupsRehome():
	if request.method == 'POST':
		kwargs = { x:request.form[x] for x in request.form if request.form[x] and request.form[x] != 'default' }
		name = kwargs['name']
		gender = kwargs['gender']
		dob = kwargs['dateOfBirth']
		weight = kwargs['weight']
		shelter_id = kwargs['shelter']
		print name + gender + dob + weight + shelter_id
		#addPup(name, gender, dob, 'none', shelter_id, weight)
		
		return render_template('pupshome.html')
	
	
	

	#vacantShelter(): 
	#returns a dictionary object that includes the id and the name 
	# of shelters with space available.
	shelters = vacantShelter()
	return render_template('pupsrehome.html', shelters=shelters)






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)