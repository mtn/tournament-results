#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    result = c.fetchall()
    conn.close()
    if result:
        return result[0][0]
    else:
        return 0


def registerPlayer(name):
    """Adds a player to the tournament database.

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players(name) VALUES(%s)", (name,))
    conn.commit()
    conn.close()


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

    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT players.id, players.name,
                 (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner) as num_wins,
                 (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner
                 OR players.id = matches.loser) as num_matches FROM players
                 ORDER BY num_wins DESC;""")
    s = c.fetchall()
    conn.commit()
    conn.close()
    return s


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner,loser) VALUES (%s,%s);" % (winner,loser))
    conn.commit()
    conn.close()


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
    standings = playerStandings()
    # print standings[0][0:2]
    pairs = zip(standings[1::2],standings[0::2])
    pairs = [ (x[0:2],y[0:2]) for (x,y) in pairs]

    conn = connect()
    c = conn.cursor()

    for pair in pairs:
        c.execute("SELECT name from players where id = (%s)" %  pair[0][0])
        name1 = c.fetchall()
        c.execute("SELECT name from players where id = (%s)" %  pair[1][0])
        name2 = c.fetchall()
        return (pair[0][0],name1[0][0],pair[1][0],name2[0][0])


reportMatch(1,2)
reportMatch(3,4)
reportMatch(1,3)
swissPairings()



