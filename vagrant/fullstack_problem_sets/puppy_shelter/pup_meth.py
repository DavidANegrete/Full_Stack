from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, Adoptor, AdoptorAndPuppy
import datetime
#specifies what db will be used
engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

#creates a stagging area to add to the db
session = DBSession()

#global variables
pupQuery = session.query(Puppy)

shelterQuery = session.query(Shelter)


def getPupsAll():
	return pupQuery.all()


#returns all the pups in ascending order A to Z
def getPupsAtoZ():
	return pupQuery.order_by(Puppy.name.asc()).all()
	#for pups in allPups:
	#	print pups.name

#querying pups younger than 6
def getBaby(var):
	#Date and time being used to do find out the yougest of pups compared to the time know
	sixMonthsfromNow = datetime.date.today() - datetime.timedelta(6 *365/12)
	youngPups = pupQuery.filter(Puppy.dateOfBirth > sixMonthsfromNow).order_by(Puppy.dateOfBirth).all()
	for pup in youngPups:
		print pup.name
		print pup.dateOfBirth
		print "_____________________________"
#takes a form date value and returns a dictionary that includs a date range.
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
	pupWeight = pupQuery.filter(Puppy.weight).order_by(Puppy.dateOfBirth).all()
	for pup in pupWeight:
		print pup.name
		print pup.weight
		print "______________________________"

def getPupsGroupByShelter():
	pupByShelterGroup = pupQuery.order_by(Puppy.shelter_id.asc()).all()
	for pup in pupByShelterGroup:
		print pup.name
		print pup.shelter_id
		print "______________________________"
#this function is used to get one shelter only
def getShelter(_id):
	return shelterQuery.filter(Shelter.id == _id).first()






#def setting the shelter cap
def setShelterCap(_id, cap):
	shelter = getShelter(_id)
	shelter.max_capacity = cap
	session.add(shelter)
	session.commit()


#inner join being used to get the the ammount of pups in the shelter
def getShelterOccupancy(_id):
	result = session.query(Puppy, Shelter).join(Shelter).filter(Shelter.id == _id).count()
	if not result:
			print "Something strange is going on"
			return
	return result

def getShelterCap(_id):
	return shelterQuery.order_by(Shelter.max_capacity).first()


def vacantShelter():
    shelters = session.query(Shelter).all()
#created dictionary//upacking shelter id + shelter name   
    o_shelter = {}
    for shelter in shelters:
        if(getShelterCap(shelter.id) >= getShelterOccupancy(shelter.id)):   
            o_shelter.update({shelter.id:str(shelter.name)})

    	return o_shelter

#this function is used to set up the name of the adoptor
def setAdoptor(name):
	adoptor =Adoptor(name=name)
	session.add(adoptor)
	session.commit





#Add a pup to find what shelter to put the pup in.

def addPup(name, gender, dateOfBirth, picture, shelter_id, weight):
	if(getShelterCap(shelter_id) >= getShelterOccupancy(shelter_id)):
		dob = datetime.strptime(dateOfBirth, '%b %d %Y')
		pupToAdd = Puppy(name = name, gender = gender, dateOfBirth = dob, picture = picture, shelter_id =shelter_id, weight = weight)
		session.add(pupToAdd)
		session.commit()
		print name + ' has been added'
	else:
		vacantShelter() 
		print "Please try again!"

			









	












	


    