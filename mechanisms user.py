import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from selenium import webdriver
import re
import time

# First we define a pair of functions to get the mechanisms then we create a dictionary for each user
# having the game names as the keys and the lists of mechanisms as the values.

# FUNCTIONS:
#
# The main page of each board game can be accessed via "https://boardgamegeek.com/boardgame/" + game_id ,
# without mentioning its "web name", ie: "https://boardgamegeek.com/boardgame/135779"
# redirects to
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"

# The list of mechanisms if found on the "credits" page (in javascript code), and not the main page.
# The credits page needs the "web name" of the boardgame, eg:
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york/credits"

# We need to get the actual page address since the name of the boardgame and
# the name on the webpage (ie the "web name") can be different:
# eg: "A Fake Artist Goes to New York" and "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"


def geturl(game_id: str) -> str:
    """
    Returns the url for bgg main page of game, given id.
    Uses regular expressions.
    :param gameid: string with the number id for game.
    :return: bgg url string.
    """
    main_page_url = "https://boardgamegeek.com/boardgame/" + game_id
    main_page = requests.get(main_page_url)
    main_page_text = main_page.text
    address_pattern = "(https://boardgamegeek.com/boardgame/[\d]+/[\w-]+)"
    address_regex = re.compile(address_pattern)
    address_find = address_regex.search(main_page_text)
    main_address = main_page_text[address_find.start():address_find.end()]
    return main_address


def getmechanisms(game_id: str, driver) -> list:
    """
    Uses regular expressions to find the list of mechanisms for a
    game on the bgg website given its number id.
    Closing browser after function recommended. gg driver.quit()
    :param driver: selenium driver, eg driver = webdriver.Firefox()
    :param game_id: string on numbers.
    :return: list of mechanisms for game.
    """
    pattern = r'(?:href=\"/boardgamemechanic.*?)>([,:\w /-]+?)<'
    regex = re.compile(pattern)
    url = geturl(game_id) + "/credits"
    # driver = webdriver.Firefox()
    driver.get(url)
    source_text = driver.page_source
    # driver.quit()
    mechanisms = regex.findall(source_text)
    return mechanisms

# DATAFRAMES AND DICTIONARIES

datafile = "Data files/Weber_bgg_data.csv"
name = "Ray&Jennie"
#datafile = "mectest.csv"

df = pd.read_csv(datafile)
# select relevant columns and drop duplicates
df = df[['objectname', 'objectid', 'yearpublished', 'itemtype']].drop_duplicates()
# remove expansions
df = df[df['itemtype'] == 'standalone']
# removing old games (before 1900)
df = df[df['yearpublished'] >= 1900]
# select relevant columns
df = df[['objectname', 'objectid']]
# converts ids from int to str
df['objectid'] = df['objectid'].astype(str)

# The following loop grabs the mechanism of each game in the data frame and appends it to a list.
mechanisms_list = []
# length of dataframe to be used in percentage of completion.
N = df.shape[0]
# opening the browser
Firefox = webdriver.Firefox()
start = time.time()
j = 1
for i, row in df.iterrows():
    mechanisms = getmechanisms(row['objectid'], Firefox)
    mechanisms_list += mechanisms
    elapsed_time = time.time() - start
    status_string = '{}\n time elapsed: {:.1f}s\n completed: {:.1f}%'.format(row['objectname'], elapsed_time, (j*100)/N)
    print(status_string)
    j +=1
print('\n')
# quit the browser
Firefox.quit()
# convert the list to a dictionary where each unique entry is a key and the number of times
# it shows up on the list is the value.
mechanisms_dict = dict(Counter(mechanisms_list))
# make a Pandas Series from the dictionary
Smec = pd.Series(mechanisms_dict)
Smec.to_csv(name + "_mechanisms.csv")
# print the 20 largest entries
ranked = Smec.nlargest(20).reset_index()
ranked.set_index(ranked.index.map(lambda x: x + 1), inplace=True)
print('Top 20 most common board game mechanisms in collection.')
print(name)
print(ranked)
