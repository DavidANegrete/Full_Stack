----
#Full Stack 
----


##About the repository 
In this repository you will find the work I completed to earn my Udacity 
Full Stack development nano-degree. It consisted of 5 projects of varying complexity
and used Python (2.7.6) as the server side programming language. 

##Files found within
Within the /vagrant directory in this repo you will find a VagrantFile that 
can be used to deploy the work, a shell script that configures the enviorment and 
each project. The projects are in their own directory, numbered from P1 to P5. 
Include in each project directory a README.md file is found with project specific
details and instructions on deploying.


##Overview
A brief overview can be found below to get an idea of work completed
for each project.

###/P1
Created server-server side code in Python and used it to store a list of 
movies including box art imagery and a movie trailer URL. This information
was then served using webpage.

###/P2
This project used a PostgreSQL database to keep track of players and 
matches in a tournament. The tournament used a Swiss system for pairing 
up players in each round.

###/P3
This application provided a list of unique items (pups) within a variety of 
categories (shelters). For this application a user registration and authentication 
system was created. Views on the app are served based on the current users state
(Signed in/Out). SQL Alchemy was used for CRUD functionality, also used was Flask to 
build the views, serve the data and serve user instances. 

###/P4
For this project a cloud-based API server was created to support a provided 
[Conference Organization](https://github.com/udacity/ud858/tree/master/ConferenceCentral_Complete) application on the web. The Google App Engine API supports the followin: user authentication, user profiles,
conference informationand various methods to query conference data.

###/P5
From a baseline installation of a Linux distribution on a virtual machine 
and I configured it to host my own web application (P3). For This project  
I created users, installed updates, secured the application from a number of attack vectors, 
and also configured both web and database servers on it. 


##Downloading and Deploying
####How to deploy the projects using the included VM. 
  1. Insure you have [Vagrant](https://www.vagrantup.com/downloads.html) installed along with a [Virtual Box](https://www.virtualbox.org/wiki/Downloads).
  2. Clone the from within your bash terminal using 
    'git clone https://github.com/DavidANegrete/Full_Stack.git'
  3. Launch the environment with the command 
    'vagrant up'
  4. Deploy the virtual machine with 
    'vagrant ssh'
  5. The modules can be found in the following directory 
    '~/vagrant'
    

####If you choose to load and deploy using your own environment
  1. Read the included README.md file for each project. 
  2. Follow the instructions as indicated using a bash terminal.

-
