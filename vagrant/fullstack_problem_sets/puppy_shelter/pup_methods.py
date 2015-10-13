from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, User, UserAndPuppy, NewFamily
from datetime import datetime as date_time
import datetime
#specifies what db will be used
engine = create_engine('sqlite:///puppyshelterwithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

#creates a stagging area to add to the db
session = DBSession()

#global variables
pupQuery = session.query(Puppy)

shelterQuery = session.query(Shelter)

def getPupsAll():
	return pupQuery.all()

#querying the db for pups younger than 6 months.
def getPuppies():
	sixMonthsfromNow = datetime.date.today() - datetime.timedelta(6 *365/12)
	return pupQuery.filter(Puppy.dateOfBirth > sixMonthsfromNow).order_by(Puppy.dateOfBirth).all()

#takes a date from a date from the possible choices to pick and returns a dictionary (YYYY-DD-MM:YYYY-DD-MM).
def getAgeRange(var):
	dateRange ={}
	if var == '5':
		today = datetime.date.today()
		ancient = datetime.date.today() - datetime.timedelta(900 *365/12)
		dateRange={ancient:today}
	elif var == '6':
		youngerThanSixMonths = datetime.date.today() - datetime.timedelta(6 *365/12)
		today = datetime.date.today()
		dateRange = {youngerThanSixMonths:today}
	elif var == '7':
		youngerThanSixMonths = datetime.date.today() - datetime.timedelta(6 *365/12)
		threeYears = datetime.date.today() - datetime.timedelta(36 *365/12)
		dateRange = {threeYears:youngerThanSixMonths}
	elif var == '8':
		threeYears = datetime.date.today() - datetime.timedelta(36 *365/12)
		sixYears = datetime.date.today() - datetime.timedelta(72 *365/12)
		dateRange = {sixYears:threeYears}
	else:
		sixYears = datetime.date.today() - datetime.timedelta(72 *365/12)
		ancient = datetime.date.today() - datetime.timedelta(300 *365/12)
		dateRange = {ancient:sixYears}
	return dateRange

#method returns a string value when an input is entered.
def getPupsByWeight():
	return pupQuery.filter(Puppy.weight).order_by(Puppy.dateOfBirth).all()

#the method returns all the pups in the db sorted by shelter_id
def getPupsGroupByShelter():
	return pupQuery.order_by(Puppy.shelter_id.asc()).all()
	
#this function is used to get one shelter only.
def getShelter(_id):
	return shelterQuery.filter(Shelter.id == _id).first()

#method to change the shelter cap if needed.
def setShelterCap(_id, cap):
	shelter = getShelter(_id)
	shelter.max_capacity = cap
	session.add(shelter)
	session.commit()

#method to get the occupancy in a given shelter.
def getShelterOccupancy(_id):
	result = session.query(Puppy, Shelter).join(Shelter).filter(Shelter.id == _id).count()
	if not result:
		return "Something strange is going on"	
	return result

#method to get the capacity in a shelter.
def getShelterCap(_id):
	result = shelterQuery.filter(Shelter.id == _id).one()
	if not result:
		return "Something strange is going on"	
	return result.max_capacity

#this method use a dictionary to return the id and name of shelter with vacancies. 
def vacantShelter():
    shelters = session.query(Shelter)
    shelter_id = {}
    for shelter in shelters:
          if(getShelterCap(shelter.id) >= getShelterOccupancy(shelter.id)):   
            shelter_id.update({shelter.id:shelter.name})
    
    return shelter_id


#this function is used to set a new user
def setUser(name, email):
	user =User(name=name, email=email)
	session.add(user)
	session.commit

#Add a pup to find what shelter to put the pup in.
def addPup(name, gender, dateOfBirth, picture, weight, shelter_id, entered_by):
	if(getShelterCap(shelter_id) >= getShelterOccupancy(shelter_id)):
		dob = getDOB(dateOfBirth)
		pupToAdd = Puppy(name = name, gender = gender, dateOfBirth = dob, picture = picture, shelter_id = shelter_id, weight = weight, entered_by=entered_by)
		session.add(pupToAdd)
		session.commit()
	else:
		return 'ALL SHELTER ARE FULL'

#Method takes a string format 'YYYY-MM-DD' and returns a date object
def getDOB(dateOfBirth):
	return date_time.strptime(dateOfBirth, '%Y-%m-%d')
