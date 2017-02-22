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



@app.route('/')
@app.route('/dliciousnails.com/')
def home():
    '''Main template for dliciousnails'''
    
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
