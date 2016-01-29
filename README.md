--
#Full Stack 
--


##What you can find in this repository 
----
In this repository you will find the work I completed to earn my Udacity 
Full Stack development nano-degree. It consisted of 5 projects of varying complexity.
The server side programming language used was Python (2.7.6). 

Within the /vagrant directory in this repo you will find a VagrantFile that 
can be used to deploy the work and a shell script that loads up the enviorment packages.
Each project, numbered as P1-P5, include a README.md file that provides project specific
details and instructions on deploying.


##Project Overview
---

####P1
Includes server-server side code in Python that is used to store a list of 
movies including box art imagery and a movie trailer URL. 

####P2
This project uses the PostgreSQL database to keep track of players and 
matches in a game tournament. The game tournament uses a Swiss system for 
pairing up players in each round.

####P3
This application provides a list of unique items (pups) within a variety of 
categories (shelters) included is a user registration and authentication 
system. Signed in and out Users have different permissions based on their 
current states.

####P4
In this project I developed a cloud-based API server to support a provided 
[Conference Organization](https://github.com/udacity/ud858/tree/master/ConferenceCentral_Complete) application that exists on the web. The API supports the following functionality, within 
Google App Engine: user authentication, user profiles, conference information
and various methods to query the conference data.

####P5
Took a baseline installation of a Linux distribution on a virtual machine 
and prepared it to host my own web application (P3). This project had me 
install updates, secure the application from a number of attack vectors, 
lastly installed and configured web and database servers.


##Downloading and Deploying
---


####How to deploy the projects using the included VM. 
-
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
-
  1. Read the included README.md file for each project. 
  2. Follow the instructions as indicated using a bash terminal.
