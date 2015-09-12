from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, Adoptor, AdoptorAndPuppy
from datetime import datetime
#specifies what db will be used
engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

#creates a stagging area to add to the db
session = DBSession()

#global variables
pupQuery = session.query(Puppy)

shelterQuery = session.query(Shelter)


#returns all the pups in ascending order A to Z
def getPupsAtoZ():
	return pupQuery.order_by(Puppy.name.asc()).all()
	#for pups in allPups:
	#	print pups.name

#querying pups younger than 6
def getPupsYoungerThanSixMonths():
	#Date and time being used to do find out the yougest of pups compared to the time know
	sixMonthsfromNow = datetime.date.today() - datetime.timedelta(6 *365/12)
	younPups = pupQuery.filter(Puppy.dateOfBirth > sixMonthsfromNow).order_by(Puppy.dateOfBirth).all()
	for pup in youngPups:
		print pup.name
		print pup.dateOfBirth
		print "_____________________________"

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


def vacantShelter():
    shelters = session.query(Shelter).all()
    print "Here are the results:"
    for shelter in shelters:
        if(shelter.max_capacity >= getShelterOccupancy(shelter.id)):
            print shelter.name + " has available space"
        else:
            print shelter.name + " is full! :("

#this function is used to set up the name of the adoptor
def setAdoptor(name):
	adoptor =Adoptor(name=name)
	session.add(adoptor)
	session.commit





#Add a pup to find what shelter to put the pup in.

def addPup(name, gender, dateOfBirth, picture, shelter_id, weight):
	if(getShelterCapacity(shelter_id) >= getShelterOccupancy(shelter_id)):
		dob = datetime.strptime(dateOfBirth, '%b %d %Y')
		pupToAdd = Puppy(name = name, gender = gender, dateOfBirth = dob, picture = picture, shelter_id =shelter_id, weight = weight)
		session.add(pupToAdd)
		session.commit()
		print name + ' has been added'
	else:
		vacantShelter() 
		print "Please try again!"

			









	












	


    