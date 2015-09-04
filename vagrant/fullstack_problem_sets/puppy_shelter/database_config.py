from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, Adoptor, AdoptorAndPuppy


#this module is used to initiate a sesion during development
def session():
	#specifies what db will be used
	engine = create_engine('sqlite:///puppyshelter.db')

	Base.metadata.bind = create_engine

	DBSession = sessionmaker(bind=engine)	

	#creates a stagging area to add to the db
	session = DBSession()
	return session