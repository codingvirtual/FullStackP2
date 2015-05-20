-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create the database
create database tournament;

-- connect to the database
\c tournament;

-- create the players and matches tables
create table players (id serial primary key, name text not null);
create table matches (winner integer not null, loser integer not null);

-- create a match_count view to tally the number of matches each player
-- has been in
create view match_count as select players.id as ID, players.name as Name, 
	count(matches.winner) as Matches_Played from players 
	left join matches on matches.winner = players.id or matches.loser = players.id 
	group by players.id;

-- create a win_count view to tally the number of wins each player has
create view win_count as select players.id as ID, players.name as Name, 
	count(matches.winner) as win_count from players 
	left join matches on matches.winner = players.id 
	group by players.id;

-- create a standings view that is built by extracting results from both the
-- match_count and win_count views. Sort the results by most wins to least wins.
create view standings as select match_count.id, match_count.name, win_count, matches_played 
	from match_count, win_count where match_count.id = win_count.id order by win_count desc;
