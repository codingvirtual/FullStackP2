UDACITY FULL-STACK NANODEGREE: PROJECT 2, TOURNAMENT RESULTS
============================================================

This project tests the student's ability create, modify & query
back-end databases using Python and PostgreSQL. The project
simulates a swiss-pairing tournament management system that
allows:

a) Players to be registered and deleted
b) Match results to be posted (winner and loser)
c) Standings to be reported
d) Pairings for next round of tournament

INSTALLATION
============

Installation assumes you already have prerequisites for the
underlying Udacity class already installed and operational.
See https://www.udacity.com/wiki/ud197/install-vagrant for 
complete details. Once you have the system operational per
that documentation, continue below.

1)	Download all files to the /vagrant/tournament directory
	on the VM. Overwrite the existing files that would have
	been created when you set up the Vagrant/VM environnment
	as described above.

2)	Launch and then ssh into the Vagrant VM (instructions
	provided in the link above)

3)	Within the VM, cd to the tournament directory by typing:

		cd /vagrant/tournament

4)	Run the psql command line tool by typing:

		psql

5)	Once in psql, import and run the file that will create
	the database and tables. NOTE to Udacity Reviewers:
	The tournament.sql file contains the commands to create
	the database itself, then connect to it, then run the
	table and view creation commands. This seemed easier
	then asking the user to manually create the database.

	To do this, type:

		\i tournament.sql

	You should see the following output:
		vagrant=> \i tournament.sql
		CREATE DATABASE
		You are now connected to database "tournament" as user "vagrant".
		CREATE TABLE
		CREATE TABLE
		CREATE VIEW
		CREATE VIEW
		CREATE VIEW

	This indicates you have successfully imported and ran
	the setup file.

6) 	Exit psql by typing:

		\q


USING THE CODE
==============

1)	From the command prompt and still in the /vagrant/tournament
	directory, you can now run the program by executing the test
	suite. Do this by typing:

		python test_tournament.py

	If successful, the output will look like this (note in 
	particular the last line indicating Success!):

		1. Old matches can be deleted.
		2. Player records can be deleted.
		3. After deleting, countPlayers() returns zero.
		4. After registering a player, countPlayers() returns 1.
		5. Players can be registered and deleted.
		6. Newly registered players appear in the standings with no matches.
		7. After a match, players have updated standings.
		8. After one match, players with one win are paired.
		Success!  All tests pass!

CREDITS / AUTHOR
================

As part of the project, Udacity provided a complete tournament_tests.py
file to test your programming with. Also provided was a skeleton file
for the main application, tournament.py. This file contained defs for each
of the required functions, but the student (myself, Greg Palen), was
responsible for creating the code for each function to allow it to
execute properly.

tournament.sql was also provided by Udacity with only the comments you
see at the top of the file. This author added all of the psql commands
for creating the database and associated tables and views.