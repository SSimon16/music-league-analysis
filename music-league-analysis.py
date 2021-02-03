### music-league-analysis.py
### Spencer Simon

##################################################
### Install & import Libraries:
# pandas, re, requests, beautifulsoup4

import pandas as pd
import re
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

##################################################
### Retrieve html documents

from pathlib import Path
html_doc = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeagueRounds-a.html').read_text()


# Parse the html file
soup = BeautifulSoup(html_doc, 'html5lib')
#print(soup.prettify())

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

for a in soup.findAll('div', attrs={'class':"round-bar complete"}):
    title = a.find('a', attrs={'class':'round-title'})
    date = a.find('span', attrs={'class':'flask-moment'})
    round_titles.append(title.text)
    round_dates.append(date.text)


#print(round_titles)
#print(round_dates)

## Round-level data for each round: Songs, Artists, Players, & Votes

# Create lists to store data
songs = []
artists = []
submitted_by = []
song_total_points = []
song_placement = []
song_vote_breakdown = [] # This will be a list of dictionaries, with players & votes cast

place = 1 # place count for song_placement

## Loop through all songs in a round
for a in soup_r1.findAll('div', attrs={'class':"song"}):
    ## find values for current song
    song_title = a.find('a', attrs={'class':'vcenter name'})
    artist = a.find('span', attrs={'class':'vcenter artist'})
    submitter = a.find('a', attrs={'href':re.compile('/user/.*')})
    points = a.find('span', attrs={'class':'point-count'})

    # for vote breakdown, get html
    soup_vb = a.find('div', attrs={'class':'vote-breakdown'})
    vote_breakdown = {}         # create dictionary to store breakdowns
    ## loop through each vote within the vote breakdown
    for b in soup_vb.findAll('div', attrs={'class':'row-fluid'}):
        voter = b.find('div', attrs={'class':'col-xs-9 col-sm-8 '
        'col-md-9 voter text-left vcenter'})
        voter_points = b.find('span', attrs={'class':'vote-count'})
        vote_breakdown[voter.text] = voter_points.text

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

# Store lists in data frames
df_song = pd.DataFrame({'Songs':songs, 'Artists':artists,
'Submitted_by':submitted_by, 'Total_points_earned':song_total_points,
'Place':song_placement
 })
df_vbreakdown = pd.DataFrame({'Songs':songs,
 'vote_breakdown':song_vote_breakdown})

# export to CSV files
df_song.to_csv('songs.csv', index=False, encoding='utf-8')
df_vbreakdown.to_csv('vote_breakdown.csv', index=False, encoding='utf-8')

##################################################
### Next Steps:
# - Create songID for songs table. Use songID instead of song name in vote_breakdown table
# - Extend Round-level data to loop through all rounds
# - create playerIDs for all players, and remove their names (so not public)
# - Reformat all raw data into normalized dataframes for database
# - Look up and include artist info (check Spotify?)
# - Reformat round_dates to be YYYY-MM-DD
# - Move data from lists into data frame & export as CSV
# -This file just for downloading data; Jupyter Notebook for EDA? Use resources
