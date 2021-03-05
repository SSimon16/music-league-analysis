### music-league-analysis.py
### Spencer Simon

################### Install & import Libraries ################################
### pandas, numpy, dt, re, requests, os, beautifulsoup4, Path

import pandas as pd
import numpy as np
import datetime as dt
import re
import requests
import os
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from pathlib import Path

###############################################################################
###############  Define functions  ############################################

def find_id(value: str, type: str, ext_value = None):
    """
    Inputs
    ------
    - value: the value we want to find the id of
    - ext_value: additional value (if needed)
    - type: the type of value (e.g. 'song', 'artist', etc.)

    Output
    ------
    Returns the id from corresponding data frame of given value and type

    For finding results_id, 1st argument (value) is the round_id, and
    2nd argument (ext_value) is the submitter_id.
    """
    if type == "song":
        match = df_song.query('title == @value').iloc[0][0]
    elif type == "artist":
        match = df_artists.query('name == @value').iloc[0][0]
    elif type == "player":
        match = df_players.query('name == @value').iloc[0][0]
    elif type == "round":
        match = df_rounds.query('name == @value').iloc[0][0]
    elif type == "result":
        match = df_results.query('round_id == @value & '
                                 'submitter_id == @ext_value').iloc[0][0]
    return match

###############################################################################
######## Retrieve html documents ##############################################
### Overall Round html file & Overall Player html file
# Note: MusicLeagueRounds html file, MusicLeaguePlayers html file, and all
# Individual Round html files should be current and downloaded in folder

# Overall Round data (last download: 3/4/2021)
from pathlib import Path
b_path = '/Users/spencersimon/Documents/Projects/Coding/music-league-analysis'

html_doc = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeagueRounds.html').read_text()

soup = BeautifulSoup(html_doc, 'html5lib')  # Parse the html file

# Overall Player data (last download: 2/16/2021)
html_doc_p = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeaguePlayers.html').read_text()

soup_p = BeautifulSoup(html_doc_p, 'html5lib')  # Parse the html file

###############################################################################
###############  Extract Overall Round & Player Data  #########################
## Overall Round Data: Round Titles & Dates
round_titles = []
dates = []
# Loop through all rounds
for a in soup.findAll('div', attrs={'class':"round-bar complete"}):
    title = a.find('a', attrs={'class':'round-title'})
    date = a.find('span', attrs={'class':'flask-moment'})
    round_titles.append(title.text)
    dates.append(date.text)

# Convert round_dates form string to DateTime
round_dates = [dt.datetime.strptime(date, '%Y-%m-%dT05:00:00Z').date()
               for date in dates]

# Makre rounds data frame
df_rounds = pd.DataFrame({'round_id': [None]*len(round_titles),
                          'name': round_titles,
                          'date': round_dates
})
# Assign round_id to df_rounds
df_rounds['round_id'] = df_rounds.groupby(['name',
                                           'date']).ngroup()


## Overall Player Data: Player names & Total points
player_names = []
player_total_points = []
for a in soup_p.findAll('div', attrs={'class':"row-fluid ranking-entry"}):
    player = a.find('span', attrs={'class':'name'})
    points = a.find('span', attrs={'class':'points'})
    player_names.append(player.text)
    player_total_points.append(points.text)

###############################################################################
######## Retrieve html documents cont. ########################################
### Individual Round html files (last download: 3/4/2021)

# list of all html file paths
html_round_docs = [Path(r'/Users/spencersimon/Documents/Projects/Coding/'
                         'music-league-analysis/MusicLeagueRound'
                         + str(i+1)
                         + '.html').read_text()
                    for i in range(len(df_rounds))]

###############################################################################
############### Extract Round Data for each round #############################
### Loop through each round html file & extract round-level data:
### Songs, Artists, Players, & Votes
songs = []
artists = []
submitted_by = []
song_total_points = []
song_placement = []
song_vote_breakdown = []  # list of lists of dictionaries w/ players & votes
song_round_names = []

for idx, i in enumerate(html_round_docs):
    html_doc_curr = html_round_docs[idx]  # Store current html file
    soup_curr = BeautifulSoup(html_doc_curr, 'html5lib')  # parse the html file

    place = 1  # place count for song_placement; reset to 1 at start of round

    # Loop through all songs in current round:
    for a in soup_curr.findAll('div', attrs={'class':"song"}):
        # find values for current song:
        song_title = a.find('a', attrs={'class':'vcenter name'})
        artist = a.find('span', attrs={'class':'vcenter artist'})
        submitter = a.find('a', attrs={'href':re.compile('/user/.*')})
        points = a.find('span', attrs={'class':'point-count'})

        vote_round_title = soup_curr.find('span',
                                           attrs={'class':'round-title'}).text

        ## for vote breakdown, get html
        soup_vb = a.find('div', attrs={'class':'vote-breakdown'})
        vote_breakdown = {}         # create dictionary to store each breakdown
        votes_breakdown_list = []   # create list to store vote_breakdown dicts

        # loop through each vote within the vote breakdown
        for b in soup_vb.findAll('div', attrs={'class':'row-fluid'}):
            voter = b.find('div', attrs={'class':'col-xs-9 col-sm-8 '
                                         'col-md-9 voter text-left vcenter'})
            voter_points = b.find('span', attrs={'class':'vote-count'})
            vote_breakdown['voter'] = voter.text
            vote_breakdown['points_given'] = voter_points.text
            vote_breakdown['round_id'] = find_id(vote_round_title, 'round')
            vote_breakdown['voted_for'] = submitter.text
            votes_breakdown_list.append(vote_breakdown)
            vote_breakdown = {}

        # append vote breakdown dictionary for current song to list
        song_vote_breakdown.append(votes_breakdown_list)

        # append values for current song to lists
        songs.append(song_title.text)
        # Remove 'By ' from artist name field
        artists.append(re.search('By (.*)', artist.text).group(1))
        submitted_by.append(submitter.text)
        song_total_points.append(points.text)
        song_placement.append(place)
        song_round_names.append(vote_round_title)
        place += 1  # increment place by 1 for next iteration of the loop

###############################################################################
######### Store lists in data frames ##########################################

df_artists = pd.DataFrame({'artist_id':[None]*len(np.unique(np.array(artists))),
                           # use np.unique to return unique values only
                           'name':np.unique(np.array(artists))
                           })
# Assign result_id to df_results
df_artists['artist_id'] = df_artists.groupby(['name']).ngroup()

df_players = pd.DataFrame({'player_id':[None]*len(player_names),
                           # use np.unique to return unique values only?
                           #'name':np.unique(np.array(player_names)),
                           'name':player_names,
                           'total_points':player_total_points
                           })
# Assign player_id to df_players
df_players['player_id'] = df_players.groupby(['name']).ngroup()

df_song = pd.DataFrame({'song_id':[None]*len(songs),
                        'title':songs,
                        'artist_id':[find_id(i, 'artist') for i in artists]
                        })
# Assign song_id to df_song
df_song['song_id'] = df_song.groupby(['title']).ngroup()

df_results = pd.DataFrame({'result_id': [None]*len(songs),
                           'place':song_placement,
                           'total_points_earned':song_total_points,
                           'submitter_id':[find_id(i, 'player')
                                           for i in submitted_by],
                           'round_id':[find_id(i, 'round')
                                        for i in song_round_names],
                           'song_id':[find_id(i, 'song') for i in songs]
                           })
# Assign result_id to df_results
df_results['result_id'] = df_results.groupby(['submitter_id',
                                              'round_id']).ngroup()

# Get lists of voter name, vote points, player who was voted for
# and round the vote was cast in, for each vote cast. And, id's.
voter_name_list = [vote['voter'] for i in song_vote_breakdown for vote in i]
id_voter_name_list = [find_id(i, 'player') for i in voter_name_list]

vote_points_list = [vote['points_given'] for i in song_vote_breakdown
                                           for vote in i]
voted_for_list = [vote['voted_for'] for i in song_vote_breakdown for vote in i]
id_voted_for_list = [find_id(i, 'player') for i in voted_for_list]

id_voted_in_round_list = [vote['round_id'] for i in song_vote_breakdown
                                             for vote in i]

# Make data frame
df_votes = pd.DataFrame({'vote_id':[None]*len(voter_name_list),
                         # Return list of values from dictionary to get points
                         'points_given':vote_points_list,
                         'voter_id':id_voter_name_list,
                         'result_id':[find_id(str(id_voted_in_round_list[idx]),
                                              'result',
                                              str(id_voted_for_list[idx]))
                                      for idx, i in enumerate(voted_for_list)]
})
# Assign vote_id to df_votes
df_votes['vote_id'] = df_votes.groupby(['voter_id',
                                        'result_id']).ngroup()


# export to CSV files
df_artists.to_csv(b_path + '/Data/artists.csv', index=False, encoding='utf-8')
df_players.to_csv(b_path + '/players.csv', index=False, encoding='utf-8')
df_song.to_csv(b_path + '/Data/songs.csv', index=False, encoding='utf-8')
df_rounds.to_csv(b_path + '/Data/rounds.csv', index=False, encoding='utf-8')
df_results.to_csv(b_path + '/Data/results.csv', index=False, encoding='utf-8')
df_votes.to_csv(b_path + '/Data/votes.csv', index=False, encoding='utf-8')

######################################################################
### Next Steps:
# - Add player demographics & ensure player info is NOT on github / not public
# - Look up and include artist info (check Spotify?)
# - This file is for scraping data; Jupyter Notebook for EDA? Use resources
