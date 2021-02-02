### music-league-analysis.py
### Spencer Simon

##################################################
### Install & import Libraries:
# requests, beautifulsoup4

import re
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

##################################################
### Retrieve html documents

from pathlib import Path
html_doc = Path('/Users/spencersimon/Documents/Projects/Coding/'
                'music-league-analysis/MusicLeagueRounds.html').read_text()


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


print(round_titles)
print(round_dates)

## Round-level data for each round: Songs, Artists, Players, & Votes

# Create lists to store data
songs = []
artists = []
submitted_by = []
song_points = []
song_placement = []
song_votes = [] # This will be a list of dictionaries, with players & votes cast

for a in soup_r1.findAll('div', attrs={'class':"song"}):
    song_title = a.find('a', attrs={'class':'vcenter name'})
    artist = a.find('span', attrs={'class':'vcenter artist'})
    submitter = a.find('a', attrs={'href':re.compile('/user/.*')})
    songs.append(song_title.text)
    artists.append(artist.text)
    submitted_by.append(submitter.text)

print(songs)
print(artists)
print(submitted_by)

##################################################
### Next Steps:
# - Extend Round-level data to loop through all rounds
# - Look up and include artist info (check Spotify?)
# - Reformat round_dates to be YYYY-MM-DD
# - Move data from lists into data frame & export as CSV
# -This file just for downloading data; Jupyter Notebook for EDA? Use resources
