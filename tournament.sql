-- Table definitions for the tournament project.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
    id serial PRIMARY KEY,
    name text );

CREATE TABLE matches (
    winner serial REFERENCES players,
    loser serial REFERENCES players);
