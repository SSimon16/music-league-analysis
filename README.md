# music-league-analysis
This repository performs data analysis of [Music League](https://musicleague.app) data for a private Music League group.

## Summary
This repository analyzes a [Music League](https://musicleague.app) group to better understand the song selections of group members and round results. In particular, this project seeks to understand the gender and racial makeup of the artists of songs submitted in the Music League. 

## Project Description

### Background
[Music League](https://musicleague.app) is an app where a group of friends compete by selecting and submitting songs that embody a chosen theme. Each week, participants have a new theme. After songs are selected, participants can view a playlist of songs via Spotify. They then vote on the songs they think best embody the theme for the week. 

Participants select one song each week. Participants have a set number of points to give to songs each week when voting that they can divide up however they want. For example, a participant could give all of their points to one song, or one point to many different songs. Participants must vote with all of their points. If they do not vote, then the song they submitted that week earns 0 points regardless of the other votes cast.

The song with the most points wins each week. Participants' points are accumulated each week to provide an overall leaderboard.

### Initial Questions, Assumptions, and Hypotheses
This project was started with the hypothesis that many participants' Music League submissions reveal a lack of diversity in their music listening preferences. This hypothesis was based on initial, anecdotal evidence gathered from participating in the Music League. 

In addition, a major assumption of this project is that participants' Music League submissions reflect their music listening preferences. While submissions do not necessarily represent all of the songs participants listen to or their favorite songs, they do represent the songs participants think to submit and are familiar with. 

#### Questions this project seeks to answer:

* Do song artists with a particular race and gender (e.g. Black women) tend to rank higher than other songs?
* Do participants show a large variance in the gender and racial diversity of their submissions?
* Are participants of a particular race and gender (e.g. white men) more likely to submit more homogeneous selections?
* Are participants more likely to submit songs with artists who share their race and/or gender?
* Has the diversity of song selections changed over time?

### Project Structure
#### File Descriptions
* [Data](https://github.com/SSimon16/music-league-analysis/tree/main/Data): Folder containing clean csv data files
  * _artists.csv_: table of artist names and information
  * _results.csv_: table of how well each submitted song did in each round, including placement and points earned
  * _rounds.csv_: table of round titles and dates
  * _songs.csv_: table of song titles and information
  * _votes.csv_: table of each vote cast
  * **Note**: players.csv is not uploaded publicly to protect the privacy of the players.
* [Images](https://github.com/SSimon16/music-league-analysis/tree/main/Images): Folder containing all images used for presentation
* [Web-Scraping_Music-League](https://github.com/SSimon16/music-league-analysis/tree/main/Web-Scraping_Music-League): Folder containing all files used for web scraping of the [Music League](https://musicleague.app) website
  * _music-league-webscrape.py_: Python file used to scrape data and export to clean csv files


#### Data Structure
ER Diagram of the database:
![ER Diagram of the database](https://github.com/SSimon16/music-league-analysis/blob/main/Images/ER-diagram.png)

Note: players.csv is not uploaded publicly to keep players' identities private.

## Questions and Feedback
Please contact Spencer Simon at spencersimon16@gmail.com with questions or feedback.
