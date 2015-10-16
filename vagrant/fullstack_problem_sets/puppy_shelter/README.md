##Pup Web Server##

This app is meant to show Oauth2 applications (Facebook and Google) as the Oauth providers and was created using a Flask framework along with SQLAlchemy as an ORM. 

**** Enviorment Details ****

A Vagrant enviorment similar tp the one used to while getting a nano degree from Udacity is needed, it can be cloned from
here.

CDN calls are made in the dead of the document (main.html) to use bootsrap for the CSS framework and JQuery Validate was also used to verify form information.

git clone http://github.com/udacity/fullstack-nanodegree-vm fullstack

*** Files Included

puppy_shelter(main folder)
	static:
		images:
		css:
	templates
		(html templates)
	client_secrets.json
	fb_client_secrets.json
	pup_methods.py
	pupwebserver.py
	pup_methods.py
	README.md

*** To Run the application
	1. clone this repository into the vagrant directory outlined in the enviorment details.
	2. Change your and go to your vagrant directory.
		(To run you VM )
		 2.1 type: vagrant ssh 
	3. Once you are in the VM and it is running, move to the directory: cd:/ puppy_shelter
	4. (1st time only)Set up the DB: type: python puppy_db_setup.py
	5. (1st time only)Populate the DB by typing : python puppy_populator.py
	6. Run the application by entering: python pupwebserver.py


*** App Details
This application allows users, to add or remove puppies from local shelters. Users are able to view puppies in local shelters and adopt them, if they are registered users. When a user first logs in, he can see what puppies are up for adoption but will only be presented with the an adopt button if logged in and if a user adds a pup in the database then he will be able to ended or delete the pups. This insures that view are limited based on the users authentication. 

***API End Point
This application provides an API endpoint usin in Javascrip Object Notation using JSONIFY. The object notation returns the name, ID and gender a pet in the system. 
The url is: /pups/<Shelter id>/shelter/JSON

*** Future applications of this app.
This application will be used to a create a Facebook application for an existing page that I am the sole administrato of called: Lost and Found Pets in El Paso. 