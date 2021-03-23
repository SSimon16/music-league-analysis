/***********************************************
**                Music League Analysis
** File:   Music League DML
** Desc:   Load data into db
** Auth:   Spencer Simon
** Date:   03/22/2021
************************************************/

USE MUSIC_LEAGUE;
SET SQL_SAFE_UPDATES = 0;

-- -----------------------------------------------------
-- Load Data from csv files
-- -----------------------------------------------------

# players.csv data
LOAD DATA LOCAL INFILE '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis/players.csv' 
INTO TABLE music_league.players 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# artists.csv data
LOAD DATA LOCAL INFILE '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis/Data/artists.csv' 
INTO TABLE music_league.artists 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# songs.csv data
LOAD DATA LOCAL INFILE '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis/Data/songs.csv' 
INTO TABLE music_league.songs 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# rounds.csv data
LOAD DATA LOCAL INFILE '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis/Data/rounds.csv' 
INTO TABLE music_league.rounds 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# results.csv data
LOAD DATA LOCAL INFILE '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis/Data/results.csv' 
INTO TABLE music_league.results 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# votes.csv data
LOAD DATA LOCAL INFILE '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis/Data/votes.csv' 
INTO TABLE music_league.votes 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;