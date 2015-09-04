============================
Tournament Swiss Pairings
============================

This Python program creates a database schema to store game matches between players, rank them and pair them up in matches in a tournament. Each player is matched up with another player that has nearly the same rank. 

-----------------
Files Included
-----------------
tournament.py
tournament.sql
tournament_test.py


---------------------------
Steps to run the program
---------------------------

Setting up the Vagrant machine:

1. Open CMD
2. Change location to the 'tournament' folder.
3. Type 'vagrant up' (if vagrant machien not running), skip to 4 if your vagrant machine is running. 
4. Type 'vagrant ssh' in the cmd terminal to connect to the Vagrant machine.

Set up the database

1. Navivate to the location within the Vagrant enviorment that has the tournament file 'cd /vagrant/tournament'
2. From within the Vagrant enviorment type in the cmd line type: 'psql \i tournament.sql' to import the database and create the database and schema.
3. Exit the PSQL terminal by typing  cntrl + D

Executing the program

1. From within the vagrant enviorment and within the tournament file (vagrant/tournament) type 'python tournamnet_test.py'


