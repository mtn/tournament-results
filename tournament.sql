-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches_and_results;

CREATE DATABASE tournament;

CREATE TABLE players (
    id smallint PRIMARY KEY,
    name text );

CREATE TABLE matches_and_results (
    match_id smallint PRIMARY KEY,
    player1 smallint,
    player2 smallint,
    winner smallint );

\c tournament

