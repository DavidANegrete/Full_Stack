-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view' 
drop database if exists tournament;
create database tournament;
\c tournament

--The players table keeps a list of players names and a primary key 'id'. 
-- 'id': primary key of the matches table
-- 'name': name of a player
CREATE TABLE players (
	id serial primary key, 
	name text
);
--The matchex table keeps a list of all the matches played and it refrences the 'id' from the players table.
-- 'match_id': primary key of the matches table
-- 'winner_id': displayes the 'id' FK of the winner
-- 'loser': displayes the 'id' FK of the loser
CREATE TABLE matches (
	match_id serial primary key, 
	winner integer references players (id), 
	loser integer references players (id)
);


INSERT INTO players (name) values ('David');
INSERT INTO players (name) values ('Darma');
INSERT INTO players (name) values ('Dad');
INSERT INTO players (name) values ('Mom');

INSERT INTO matches (winner, loser) values (2,1);
INSERT INTO matches (winner, loser) values (2,3);
INSERT INTO matches (winner, loser) values (2,4);
INSERT INTO matches (winner, loser) values (1,4);
INSERT INTO matches (winner, loser) values (1,3);
INSERT INTO matches (winner, loser) values (3,4);
