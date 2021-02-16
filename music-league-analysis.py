### music-league-analysis.py
### Spencer Simon

##################################################
### Install & import Libraries:
# pandas, re, requests, beautifulsoup4

import pandas as pd
import numpy as np
import re
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

##################################################
### Define functions

def find_id(value: str, type: str):
    """
    Inputs
    ------
    - value: the value we want to find the id of
    - type: the type of value (e.g. 'song', 'artist', etc.)

    Output
    ------
    Returns the id from corresponding data frame of given value and type
    """
    # Since protocols are read in order of rank, skaterNumber 1 = event_rank 1, etc.
    if type == "song":
        match = df_song.query('title == @value').iloc[0][0]
    elif type == "artist":
        match = df_artists.query('name == @value').iloc[0][0]
    elif type == "player":
        match = df_players.query('name == @value').iloc[0][0]
    return match


##################################################
### Retrieve html documents

# Overall Round data (last download: 2/16/2021)
from pathlib import Path
html_doc = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeagueRounds.html').read_text()


# Parse the html file
soup = BeautifulSoup(html_doc, 'html5lib')

# Overall Player data (last download: 2/16/2021)
html_doc_p = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeaguePlayers.html').read_text()


# Parse the html file
soup_p = BeautifulSoup(html_doc_p, 'html5lib')

# Round 1 data (last download: 2/16/2021)
html_doc_r1 = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeagueRound1.html').read_text()


# Parse the html file
soup_r1 = BeautifulSoup(html_doc_r1, 'html5lib')

##################################################
### Extract data

## Overall Round Data: Round Titles & Dates
# Create lists to store data
round_titles = []
round_dates = []
# Loop through all rounds
for a in soup.findAll('div', attrs={'class':"round-bar complete"}):
    title = a.find('a', attrs={'class':'round-title'})
    date = a.find('span', attrs={'class':'flask-moment'})
    round_titles.append(title.text)
    round_dates.append(date.text)

## Overall Player Data: Player names & Total points
# Create lists to store data
player_names = []
player_total_points = []
for a in soup_p.findAll('div', attrs={'class':"row-fluid ranking-entry"}):
    player = a.find('span', attrs={'class':'name'})
    points = a.find('span', attrs={'class':'points'})
    player_names.append(player.text)
    player_total_points.append(points.text)

## Round-level data for each round: Songs, Artists, Players, & Votes
# Create lists to store data
songs = []
artists = []
submitted_by = []
song_total_points = []
song_placement = []
# This will be a list of dictionaries, with players & votes cast
song_vote_breakdown = []
place = 1 # place count for song_placement
# Loop through all songs in a round
for a in soup_r1.findAll('div', attrs={'class':"song"}):
    ## find values for current song
    song_title = a.find('a', attrs={'class':'vcenter name'})
    artist = a.find('span', attrs={'class':'vcenter artist'})
    submitter = a.find('a', attrs={'href':re.compile('/user/.*')})
    points = a.find('span', attrs={'class':'point-count'})

    # for vote breakdown, get html
    soup_vb = a.find('div', attrs={'class':'vote-breakdown'})
    vote_breakdown = {}         # create dictionary to store breakdowns
    round_num = 1               # set init round number
    ## loop through each vote within the vote breakdown
    for b in soup_vb.findAll('div', attrs={'class':'row-fluid'}):
        voter = b.find('div', attrs={'class':'col-xs-9 col-sm-8 '
        'col-md-9 voter text-left vcenter'})
        voter_points = b.find('span', attrs={'class':'vote-count'})
        vote_breakdown[voter.text] = [voter_points.text, round_num]

    # append vote breakdown dictionary for current song to list
    song_vote_breakdown.append(vote_breakdown)

    ## append values for current song to lists
    songs.append(song_title.text)
    # Remove 'By ' from artist name field
    artists.append(re.search('By (.*)', artist.text).group(1))
    submitted_by.append(submitter.text)
    song_total_points.append(points.text)
    song_placement.append(place)
    place += 1 # increment place by 1 for next iteration of the loop

##############################
### Store lists in data frames

df_artists = pd.DataFrame({'artist_id':[None]*len(artists),
                           # use np.unique to return unique values only
                           'name':np.unique(np.array(artists))
})
# Assign result_id to df_results
df_artists['artist_id'] = df_artists.groupby(['name']).ngroup()

df_players = pd.DataFrame({'player_id':[None]*len(player_names),
                           # use np.unique to return unique values only
                           'name':player_names,
                           'total_points':player_total_points
})
# Assign player_id to df_players
df_players['player_id'] = df_players.groupby(['name']).ngroup()

df_song = pd.DataFrame({'song_id':[None]*len(songs),
                        'title':songs,
                        'artist_id':[find_id(i, 'artist')
                                     for i in artists]
})
# Assign song_id to df_song
df_song['song_id'] = df_song.groupby(['title']).ngroup()

df_results = pd.DataFrame({'result_id': songs,
                           'place':song_placement,
                           'total_points_earned':song_total_points,
                           'submitter_id':[find_id(i, 'player')
                                           for i in submitted_by],
                           'song_id':[find_id(i, 'song')
                                      for i in songs]
})
# Assign result_id to df_results
df_results['result_id'] = df_results.groupby(['submitter_id'] # **ADD round_id here
                                             ).ngroup()


# loop through song_vote_breakdown list, then loop through each element of
# each dictionary in the list, to get lists of vote data
vote_dict_voters = [j for idx, i in enumerate(song_vote_breakdown)
                        for j in list(song_vote_breakdown[idx].keys())]
vote_dict_points = [j[0] for idx, i in enumerate(song_vote_breakdown)
                           for j in list(song_vote_breakdown[idx].values())]
vote_dict_rounds = [j[1] for idx, i in enumerate(song_vote_breakdown)
                           for j in list(song_vote_breakdown[idx].values())]
# Make data frame
df_votes = pd.DataFrame({'vote_id':[None]*len(vote_dict_voters),
                         # Return list of values from dictionary to get points
                         'points_given':vote_dict_points,
                         'voter_id':[find_id(i, 'player')
                                    for i in vote_dict_voters],
                         'result_id':[None]*len(vote_dict_voters)
})
# Assign vote_id to df_votes
df_votes['vote_id'] = df_votes.groupby(['voter_id'] # **ADD round_id here
                                             ).ngroup()


# export to CSV files
df_artists.to_csv('artists.csv', index=False, encoding='utf-8')
df_players.to_csv('players.csv', index=False, encoding='utf-8')
df_song.to_csv('songs.csv', index=False, encoding='utf-8')
df_results.to_csv('results.csv', index=False, encoding='utf-8')
df_votes.to_csv('votes.csv', index=False, encoding='utf-8')

##################################################
### Next Steps:
# - Make round table, and add round_id to results table, so I can then
# add result_id to votes table
# - Extend Round-level data to loop through all rounds & add round id's and df
# - When upload data files: ensure player names are NOT on github so not public
# - Reformat all raw data into normalized dataframes for database
# - Look up and include artist info (check Spotify?)
# - Reformat round_dates to be YYYY-MM-DD
# -This file just for downloading data; Jupyter Notebook for EDA? Use resources
