-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create database tournament;
\c tournament;
create table players (id serial primary key, name text not null);
create table matches (winner integer not null, loser integer not null);
create view match_count as select players.id as ID, players.name as Name, 
	count(matches.winner) as Matches_Played from players 
	left join matches on matches.winner = players.id or matches.loser = players.id 
	group by players.id;
create view win_count as select players.id as ID, players.name as Name, 
	count(matches.winner) as win_count from players 
	left join matches on matches.winner = players.id 
	group by players.id;
create view standings as select match_count.id, match_count.name, win_count, matches_played 
	from match_count, win_count where match_count.id = win_count.id order by win_count desc;
