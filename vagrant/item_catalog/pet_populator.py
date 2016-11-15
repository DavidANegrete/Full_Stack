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

description = "Lorem ipsum dolor sit amet, eu mauris dis at donec non, aliquam et felis morbi duis, \
	vel morbi nulla facilisi rhoncus enim ipsum, posuere nec sodales. Tellus vel, nunc luctus lorem. \
	Tristique justo ullamcorper justo, fringilla suscipit sed eget"

dog_pictures = [
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-9/14639723_659730804200225_6113168071590213186_n.jpg?oh=ab6772ba661a80d4f66453fe23708d7e&oe=58C86177",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/q83/p200x200/14691091_655475204625785_3363591184912705123_n.jpg?oh=9b989e18617869dc0f68eace2f4529c0&oe=58CF4493",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/p200x200/14650446_650579905115315_4874248687599002450_n.jpg?oh=a12f75a9d2a8922122189725f016eade&oe=58D53E35",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/c0.1.200.200/p200x200/14291764_639527822887190_7911783569290494441_n.jpg?oh=5d48f29fafb4391d5946fe28a0140bd8&oe=58C9BF70",
		"https://scontent-dft4-1.xx.fbcdn.net/v/t1.0-0/c0.1.200.200/p200x200/13939489_625187744321198_8672350428679549280_n.jpg?oh=4d43f7859dbebc74228a85307ae7d0b2&oe=58C73887"
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

	last_user = session.query(User).order_by(User.id.desc()).first()

	if random.choice(animal_types).lower() == "dog":
		new_pet = Pet(
			animal_type = random.choice(animal_types),
			description= description, gender = "male",
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

	if random.choice(animal_types).lower() == "cat":
		new_pet = Pet(
			animal_type = random.choice(animal_types),
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

# adds the male pups
female_pets_added = 0	
for i, x in enumerate(female_names):
	
	new_user = User(name=create_random_user(), email=create_random_email())
	session.add(new_user)
	session.commit()

	last_user = session.query(User).order_by(User.id.desc()).first()

	if random.choice(animal_types).lower() == "dog":
		new_pet = Pet(
			animal_type = random.choice(animal_types),
			description= description, gender = "female",
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

	if random.choice(animal_types).lower() == "cat":
		new_pet = Pet(
			animal_type = random.choice(animal_types),
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
		female_pets_added = 1 + female_pets_added

pets = female_pets_added + male_pets_added
print 'Male Pets Added: ' + str(female_pets_added)
print 'Female Pets Added: ' + str(male_pets_added)
print 'Pets Added : ' + str(pets)