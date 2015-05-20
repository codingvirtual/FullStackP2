#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

"""
    This application relies on a PostgreSQL database named "tournament."
    The set up of this database is reflected in tournament.sql which can be
    imported into PostgreSQL using \i tournament.sql.

    The database consists of two tables:
        players: a database of registered players
            id: a unique id number for the player (primary key)
            name: the player's full name as a single text element
        matches: a database of the winner and loser of each match
            winner: the id of the winning player (used as a foreign key to players)
            loser: the id of the losing player (again, foreign key to players)

    There are also several Views that make table qeuries easier:
        match_count: provides a concise table of how many matches each player
            has been in. Used by the standings view further down.
                id: the id of the player
                name: name of the player
                matches_played: count of number of matches the player has been in
        win_count: provides a concise table of how many wins each player has had. Used
            by the standings view further down.
                id: the id of the player
                name: name of the player
                win_count: number of wins for this player
        standings: a concise table of current standings sorted in order from
            most wins to least wins. It queries the other two views to compose
            its results and extract wins and matches played for each player.
                id: the id of the player
                name: name of the player
                win_count: number of wins for this player
                matches_played: total number of matches the player has been in
"""

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    """ the following command removes all rows from table 'matches' """
    c.execute("DELETE from matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    """ the following command removes all rows from table 'players' """
    c.execute("DELETE from players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    """ This query counts the number of rows in the players table, which
    represents the total number of registered players """

    c.execute("SELECT count(*) from players;")
    player_count = c.fetchone()   """ should only be one record """
    db.close()
     """ the count will be the only element in this list, so return it """
    return player_count[0]  

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    c = db.cursor()
    """ need only insert the name. The ID field is configured as 'serial'
    so the database will automatically assign the next number in the sequence.
    Since it is a primary key, it is guaranteed to also be unique. Note that
    there can be multiple occurrences of a player with the same name, but each
    will have a unique ID in the database """
    c.execute("INSERT INTO players (name) values (%s);",(name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    """ Using the standings view to easily extract current standings """
    c.execute("SELECT * FROM standings")
    """ put the query results into a list and then return that list. Note
    that the standings table will include players who have not yet played
    at all (zero matches) as well as players who have never won """
    result = c.fetchall()
    db.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    """ add a new record to the matches table reflecting the result """
    c.execute("INSERT INTO matches (winner, loser) values (%s, %s);",(winner, loser))
    db.commit()
    db.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()

    """ standings are in order from most wins to most losses. The basic approach
    of the Swiss Pairing is to take the first two players in the standings and
    match them up, then the next two, etc. This query gets all standings records
    and assumes there will always be an even number of players. """
    c.execute("SELECT id, name FROM standings")

    result = c.fetchall()

    """ initialize a list to contain the pairing tuples """
    pairings=[]

    """ iterate over the standings. The "current" record in the list (represented
    by x) is used to retrieve the id and name of the first player and x+1 is
    used to get the opponent. X is then incremented by two to get the next pair """
    for x in range(0,len(result) - 1,2):

        """ create a tuple consisting of the first player id and name concatenated
        with the 2nd player id and name. Append this to the pairings list """
        pairings.append(result[x] + result[x+1])
    db.close()

    """ return the pairings list of tuples """
    return pairings
