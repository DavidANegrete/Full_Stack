from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, Adoptor, AdoptorAndPuppy
from pup_meth import * 
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

#search for a pup 
@app.route('/pups/search/', methods=['GET', 'POST'])
def pupsSearch():
	shelters = shelterQuery.all()
	if request.method == 'POST':
		if request.form['name']:
			name = request.form['name']
		else:
			name = 'any'
		if request.form['gender']:
			gender = request.form['gender']
		if request.form['age-option']:
			age_option = request.form['age-option']
		if request.form['shelter_id']:
			shelter_id = request.form['shelter_id'] 

		return redirect(url_for('searchResults', name = name, gender=gender,
							 age_option=age_option, shelter_id=shelter_id ))
	return render_template('pupssearch.html', shelters=shelters)

@app.route('/pups/search/results/<name>/<gender>/<age_option>/<shelter_id>', methods=['GET', 'POST'])
def searchResults(name, gender, age_option, shelter_id):
	return render_template('searchresults.html', name=name, gender=gender,
	age_option=age_option, shelter_id=shelter_id)


@app.route('/pups/adopt/')
def pupsAdopt():
	return render_template('pupsadopt.html')

@app.route('/pups/rehome/')
def pupsRehome():
	return render_template('pupsrehome.html')






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)