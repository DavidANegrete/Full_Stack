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



@app.route('/')
@app.route('/pups/', methods=['GET', 'POST'])
def pups():
	return render_template('pupshome.html')

@app.route('/pups/search/')
def pupsSearch():
	return render_template('pupssearch.html')

@app.route('/pups/adopt/')
def pupsAdopt():
	return render_template('pupsadopt.html')

@app.route('/pups/add/')
def pupsAdd():
	return render_template('pupsadd.html')






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)