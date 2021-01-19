### music-league-analysis.py
### Spencer Simon

##################################################
### Install & import Libraries
#pip install requests
#pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup

##################################################
### Retrieve html

# Specify Music League website URL
URL = 'https://musicleague.app/l/5f7fd2714a7bfd000f0c46cc/'
# Retrieve web page data from the URL
page = requests.get(URL)
page.encoding = 'utf-8'   # set encoding

# create a Beautiful Soup object
soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find_all('div', class_='round-bar')

print(page.text)
