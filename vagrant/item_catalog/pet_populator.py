from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pet_db_setup import Base, Pet, User, Status
from random import randint
import datetime
import random

engine = create_engine('sqlite:///lostandfoundpets.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Creating random pet 

users = [
		"David", "Udarmaa", "Joe", "Tony", 
		"Siria", "Chuka", "Booboo", "Boloroo", 
		"Macie", "Virginia", "Mary"]

male_names = [
			"Bailey", "Max", "Charlie", "Buddy","Rocky", "Jake", "Jack",
			"Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley",
			"Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", 
			"Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", 
			"Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", 
			"Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", 
			"Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = [
				'Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 
				'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 
				'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 
				'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 
				'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 
				'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

animal_types = [ "Dog", "Cat",]

random_gender = ["male", "female"]

description = "Lorem ipsum dolor sit amet, eu mauris dis at donec non, aliquam et felis morbi duis, \
	vel morbi nulla facilisi rhoncus enim ipsum, posuere nec sodales. Tellus vel, nunc luctus lorem. \
	Tristique justo ullamcorper justo, fringilla suscipit sed eget"

dog_pictures = [
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/15036709_670137353159570_3407299480044822721_n.jpg?oh=1bcfd36954ac18e500bf18d09bebca4b&oe=5889D26E",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/15095123_668613856645253_2572089876212301235_n.jpg?oh=d5aeb6fa46332adf8f897ec2d57b0926&oe=58D496DA",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/14962618_667077596798879_1408085574771633721_n.jpg?oh=a4b8a5f5a1c3f294d1fa8e27f29ac824&oe=58CA29AE",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/14947555_663376803835625_9164914377689163469_n.jpg?oh=7591bb4359fdb40dbc53aaf5e43538cc&oe=58C2ED15"
]

cat_pictures =[
"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/14642378_658195294353776_4322344447020511845_n.jpg?oh=8dc43c8c6f22b2f0802e2bee50f6d0a4&oe=58D3602E",
"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/14604854_649387741901198_2319356974123048754_n.jpg?oh=c1c00b6598e0ef55af8776e45666963c&oe=58D33FC7",
"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/c1.0.200.200/p200x200/14570390_646557528850886_1806117314747102261_n.jpg?oh=56c0c00fba49618f156426bab8a46559&oe=58C2873C",
"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/14095748_628659863973986_8615838207538585033_n.jpg?oh=3d092b2582217494f6a79604ff652619&oe=58C82539"
]

zipcodes = [
		"79936", "79912", "79924", "79927", "88008",
		"79932", "79934", "79849", "79835", "79908", 
		"79916", "79821", "79928"]

description = "Lorem ipsum dolor sit amet, eu mauris dis at donec non, aliquam et felis morbi duis, \
	vel morbi nulla facilisi rhoncus enim ipsum, posuere nec sodales. Tellus vel, nunc luctus lorem. \
	Tristique justo ullamcorper justo, fringilla suscipit sed eget"

current_status = ['Lost', 'Found', 'On the Run']

def create_random_email():
	''' This method creates a random email address'''
	_verb=['cool', 'nice','verrynoice', 'funny', 'hangry', 'focused', 'master', 'artistic']
	_animal=['rabbit','squid','sheppard','bird','lion','snake']
	_numbers=['678','247','789', '12', '10', '79', '80', '90']
	_domain=['@gmail.com','@yahoo.com','@msn.com', '@aol.com']

	return random.choice(_verb)+random.choice(_animal)+random.choice(_numbers)+random.choice(_domain)

def create_random_user():
	picked_choice=randint(1,3)
	if picked_choice == 1:
		return random.choice(male_names)
	elif picked_choice == 2:
		return random.choice(female_names)
	else:
		return random.choice(users)

# creates a random email
def create_random_email():
	_verb=['cool', 'nice','verrynoice', 'funny', 'hangry', 'focused', 'master', 'artistic']
	_animal=['rabbit','squid','sheppard','bird','lion','snake']
	_numbers=['678','247','789', '12', '10', '79', '80', '90']
	_domain=['@gmail.com','@yahoo.com','@msn.com', '@aol.com']

	return random.choice(_verb)+random.choice(_animal)+random.choice(_numbers)+random.choice(_domain)


# adds the male pups
male_pets_added = 0	
for i, x in enumerate(male_names):
	new_user = User(name=create_random_user(), email=create_random_email())
	session.add(new_user)
	session.commit()

	last_user = session.query(User).order_by(User.id).first()
	random_choice = random.choice(animal_types).lower()

	if random_choice == "dog":
		new_pet = Pet(
			animal_type = random_choice,
			description= description,
			gender = "male",
			name = x,
			picture = random.choice(dog_pictures),
			zipcode= random.choice(zipcodes))
		session.add(new_pet)
		session.commit()
		last_pet = session.query(Pet).order_by(Pet.id.desc()).first()
		if random.choice(current_status).lower() == "lost":
			status = Status(
				is_lost = True,
				is_found = False,
				on_the_run = False,
				pet_id = last_pet.id,
				entered_by =last_user.id
				)
			session.add(status)
			session.commit()
		if random.choice(current_status).lower() == "found":
			status = Status(
				is_lost = False,
				is_found = True,
				on_the_run = False,
				pet_id = last_pet.id,
				entered_by =last_user.id
				)
			session.add(status)
			session.commit()
		if random.choice(current_status).lower() == "run":
			status = Status(
				is_lost = False,
				is_found = False,
				on_the_run = True,
				pet_id = last_pet.id,
				entered_by =last_user.id
				)
			session.add(status)
			session.commit()

	random_choice = random.choice(animal_types).lower()
	if random_choice == "cat":
		new_pet = Pet(
			animal_type = random_choice,
			description= description, gender = "male",
			name = x,
			picture = random.choice(cat_pictures),
			zipcode= random.choice(zipcodes))
		session.add(new_pet)
		session.commit()
		last_pet = session.query(Pet).order_by(Pet.id.desc()).first()
		if random.choice(current_status).lower() == "lost":
			status = Status(
				is_lost = True,
				is_found = False,
				on_the_run = False,
				pet_id = last_pet.id,
				entered_by =last_user.id
				)
			session.add(status)
			session.commit()
		if random.choice(current_status).lower() == "found":
			status = Status(
				is_lost = False,
				is_found = True,
				on_the_run = False,
				pet_id = last_pet.id,
				entered_by =last_user.id
				)
			session.add(status)
			session.commit()
		if random.choice(current_status).lower() == "on_the_run":
			status = Status(
				is_lost = False,
				is_found = False,
				on_the_run = True,
				pet_id = last_pet.id,
				entered_by =last_user.id
				)
			session.add(status)
			session.commit()
		male_pets_added = 1 + male_pets_added



pets =  male_pets_added

print 'male Pets Added: ' + str(male_pets_added)
print 'Pets Added : ' + str(pets)