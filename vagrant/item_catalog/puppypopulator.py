from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, User, UserAndPuppy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelterwithusers.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Add Shelters
shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zipCode = "94601", website = "oaklandanimalservices.org", max_capacity = 19)
session.add(shelter1)

shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode = "94103", website = "sfspca.org", max_capacity = 25)
session.add(shelter2)

shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zipCode = "94103", website = "http://wonderdogrescue.org", max_capacity = 20)
session.add(shelter3)

shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zipCode = "94501", website = "hsalameda.org", max_capacity = 30)
session.add(shelter4)

shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", website = "paloaltohumane.org", max_capacity = 20)
session.add(shelter5)

# Creating random pup entries into the db 

male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = ["https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcS23cFdgWUSdouxxvOI1kqj-kmy_cDUHOSoFexKzbjf6HPlRRoc7g", "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSUV1cHruejy3e7nrm-QAJQCS84AyMfGjBWMhUXOPU3hftBoKGQ", "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQyGYt_NJuH1qlTfsV-gmsJLADPCa-BKR6CEnxqNPXnU_mzAhWG","https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcREODRtozKbqRp-mzsHwx9D6H1SaYQZJvHwm2j433hXrAXFsDaMZg", "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcS4KbI3B8Gkifzn0tpbreojPU8NZTRe6zh0XapP6CBiFH3fnnzT", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-da5zxJsXuM0bIB6qsYCwfqOhJ8sc7stY3EQNZ5-Cv54amIqV", "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcS4cpScUUWaz_7HUVLSHOob6-Bod9ei6RIzK09tGf4qxqT9qoaY", "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQmzP_S6ujFYhfCuyRkvHNzMNzLMHY0HpBwbgvVRgO3SujrH6jH0", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn4rWVN3bC_rRY-TWsOucRQgIfijBc_9FB2Vsz6mPa1DbU8Mxu","https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQKaRL2xE3FDM1QGrDnhZ6-602x7Q2ChPaqYupsVabpsxDndDRD", "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcR3sOB4VJ-fYJQasfDk4tPXw-MbORJh1h3WaNbr-5fa0iFsHOze2Q","https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQjYGFQslvGYgj1qoVqNSfC0Il1U_7FPmP_q618x9FarAdTnwhJ", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHQAIHOvdenhh_2saKT2aU5nXhUt9tR1nFEcob5qTnwCnWIzj-", "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSihUMFr5svoqtLZajX0EJY46DzSR1ELyu841FIFHHT4QNHGTR1", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_w6RqlkAijsUlCpg3Qa3OIVOZ6ojMQ_1NOyZKLOzz0fEMQkTa", "data:image/jpeg;base64,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", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCGZgQU_uOMYCmucqQzVQbvBenhpxjWOScYHNip5QS0HVYRCBhOA", "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSkWJ5IMUYmQTz2sQnh49kR9XP8sd5UZyNEluCK08rMQpeIm2Q9tg"]

users = ["David","Udarmaa", "Joe", "Tony", "Siria", "Chuka", "Booboo", "Boloroo", "Macie", "Virginia", "Mary"]

# This method will make a random age for each puppy between 0  and 7 years old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,2555)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

# This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

	# This method creates a random user.

def CreateRandomUserName():
	picked_choice=randint(1,3)
	if picked_choice == 1:
		return random.choice(male_names)
	elif picked_choice == 2:
		return random.choice(female_names)
	else:
		return random.choice(users)

# creates a random email
def CreateRandomEmail():
	_verb=['cool', 'nice','verrynoice', 'funny', 'hangry', 'focused', 'master', 'artistic']
	_animal=['rabbit','squid','sheppard','bird','lion','snake']
	_numbers=['678','247','789', '12', '10', '79', '80', '90']
	_domain=['@gmail.com','@yahoo.com','@msn.com', '@aol.com']

	return random.choice(_verb)+random.choice(_animal)+random.choice(_numbers)+random.choice(_domain)

# adds the male pups
male_pups_added = 0	
for i,x in enumerate(male_names):
	
	new_user = User(name=CreateRandomUserName(),email=CreateRandomEmail())
	session.add(new_user)
	session.commit()

	last_user = session.query(User).order_by(User.id.desc()).first()

	new_puppy = Puppy(entered_by = last_user.id, name = x, gender = "male", dateOfBirth = CreateRandomAge(), picture=random.choice(puppy_images), shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()
	male_pups_added = 1 + male_pups_added

#adds the female pups
female_pups_added = 0
for i,x in enumerate(female_names):

	new_user = User(name=CreateRandomUserName(),email=CreateRandomEmail())
	session.add(new_user)
	session.commit()

	last_user = session.query(User).order_by(User.id.desc()).first()

	new_puppy = Puppy(entered_by = last_user.id, name = x, gender = "female", dateOfBirth = CreateRandomAge(), picture=random.choice(puppy_images), shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()
	female_pups_added= 1 + female_pups_added

pups = male_pups_added+female_pups_added
print 'Male Pups Added: ' + str(male_pups_added)
print 'Female Pups Added: ' + str(female_pups_added)
print 'Added By User: ' + str(pups)