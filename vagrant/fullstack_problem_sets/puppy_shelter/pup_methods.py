from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, User, UserAndPuppy, NewFamily
from datetime import datetime as date_time
import datetime
# Specifies what db will be used
engine = create_engine('sqlite:///puppyshelterwithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

# Creates a stagging area to add to the db
session = DBSession()

# Global variables
pupQuery = session.query(Puppy)

shelterQuery = session.query(Shelter)

pupAndShelter = session.query(Puppy, Shelter)


def getPupsAll():
	return pupQuery.all()


# This method gets an age range when a number is entered from 5-9
# This method is used when a age range is selected as a search criteria.
def getAgeRange(var):
	
	''' Takes in number in string format from 5-9 and returns and age range,
	in a key value pair. The key is the most current of dates. Today is set
	using the datetime module, to get the date of today. '''
	
	dateRange ={}

	today = datetime.date.today()

	if var == '5':
		today = today
		ancient = today - datetime.timedelta(900 * 365 / 12)
		dateRange={ancient:today}
	elif var == '6':
		youngerThanSixMonths = today - datetime.timedelta(6 * 365 / 12)
		today = datetime.date.today()
		dateRange = {youngerThanSixMonths:today}
	elif var == '7':
		youngerThanSixMonths = today - datetime.timedelta(6 * 365 / 12)
		threeYears = today - datetime.timedelta(36 * 365 / 12)
		dateRange = {threeYears:youngerThanSixMonths}
	elif var == '8':
		threeYears = today - datetime.timedelta(36 * 365 / 12)
		sixYears = today - datetime.timedelta(72 * 365 / 12)
		dateRange = {sixYears:threeYears}
	else:
		sixYears = today - datetime.timedelta(72 * 365 / 12)
		ancient = today - datetime.timedelta(300 * 365 / 12)
		dateRange = {ancient:sixYears}
	return dateRange

	
# This method is used to get one shelter only.
def getShelter(_id):

	'''	Method returns a sheleter object when a shelter id is entered.'''

	return shelterQuery.filter(Shelter.id == _id).first()

# Method to change the shelter cap if needed.
def setShelterCap(_id, cap):

	'''	This is a setter method to change the shelters capacity	'''

	shelter = getShelter(_id)
	shelter.max_capacity = cap
	session.add(shelter)
	session.commit()


# Method gets the occupancy in a given shelter.
def getShelterOccupancy(_id):

	''' This method returns back the capacity in a shelter 
	when a shelter id is entered. '''

	result = pupAndShelter.join(Shelter).filter(Shelter.id == _id).count()
	if not result:
		return "Something strange is going on"	
	return result

# Method returns the capacity in a shelter.
def getShelterCap(_id):

	'''	Method the capacity in a shelter. Takes in a shelter id. '''

	result = shelterQuery.filter(Shelter.id == _id).one()
	if not result:
		return "Something strange is going on"	
	return result.max_capacity


# This method use a dictionary to return the id and name of shelter with vacancies. 
def vacantShelter():

	'''method returns vacant shelters'''
	
	shelters = session.query(Shelter)
	shelter_id = {}
	for shelter in shelters:
		if(getShelterCap(shelter.id) >= getShelterOccupancy(shelter.id)):
			shelter_id.update({shelter.id:shelter.name})
			return shelter_id

# Add a pup to find what shelter to put the pup in.
def addPup(name, gender, dateOfBirth, picture, weight, shelter_id, entered_by):

	''' Method creates a new puppy object, it uses getDOB to 
	turn a string to a datetime object. '''

	if(getShelterCap(shelter_id) >= getShelterOccupancy(shelter_id)):
		dob = getDOB(dateOfBirth)
		pupToAdd = Puppy(name = name, gender = gender, dateOfBirth = dob, 
			picture = picture, shelter_id = shelter_id, weight = weight, 
			entered_by=entered_by)
		session.add(pupToAdd)
		session.commit()
	else:
		return 'ALL SHELTER ARE FULL'

# Create new family
def newFam(adopter_id, adopter_name, puppy_id, puppy_name, shelter_id, ):

	''' Method inserts the followiing to the NewFamily table: 
	adopter_id(User.id), adopter_name(User.name), (Puppy.id), 
	(Puppy.name), (Shelter.id) '''

	newFam = NewFamily(adopter_id = adopter_id,
		adopter_name = adopter_name, puppy_id = puppy_id,
		puppy_name = puppy_name, shelter_id = shelter_id)
	session.add(pupToAdd)
	session.commit


# Method takes a string format 'YYYY-MM-DD' and returns a date object
def getDOB(dateOfBirth):

	''' Here in the method I used the datetime module to convert a 
	string to a date object. This was created because I was not able 
	to insert a string as a date in the database. '''

	return date_time.strptime(dateOfBirth, '%Y-%m-%d')