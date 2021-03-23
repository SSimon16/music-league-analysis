/***********************************************
**                Music League Analysis
** File:   Music League SQL
** Desc:   SQL Queries
** Auth:   Spencer Simon
** Date:   03/22/2021
************************************************/

USE MUSIC_LEAGUE;

# Show the number of songs submitted by each artist and average points per song by them
SELECT 
	artists.name,
    COUNT(*) as song_count,
    SUM(total_points_earned),
    SUM(total_points_earned) / COUNT(*) as avg_points
FROM
	artists
		INNER JOIN
	songs ON artists.artist_id = songs.artist_id
		INNER JOIN
	results ON songs.song_id = results.song_id
GROUP BY artists.artist_id
ORDER BY 4 DESC;

# Show the total points each player has given each other player
SELECT
    pV.name as voter_name,
    votes.voter_id,
    SUM(votes.points_given),
    results.submitter_id,
    pS.name as submitter_name
FROM
	votes
		INNER JOIN
	results ON votes.result_id = results.result_id
		INNER JOIN
	players pS ON results.submitter_id = pS.player_id
		INNER JOIN
	players pV ON votes.voter_id = pV.player_id
GROUP BY votes.voter_id, results.submitter_id
ORDER BY 2 DESC, 3 DESC;