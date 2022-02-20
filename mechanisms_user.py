# Running this script will print a list of the top 20 most common
# mechanisms for the games in a user's collection. It will also
# create a csv file with two columns: one for the mechanisms and the
# other for the number of games in which they apper for the user.
#
# To fetch the mechanisms of a game, we will need to access the
# bgg website, and we do so via url requests (to find each game's
# mechanisms page from its main page) and via a Selenium WebDriver
# (to grab the list of mechanisms in the javascript code). Thus
# running this script will result in the opening of an automated
# browser window.
#
# The script expects the csvfile obtained when one downloads collection
# data from boardgamegeek.com. For an explanation on how to obtain
# this, see https://boardgamegeek.com/wiki/page/Data_Mining
#
# First we define a pair of functions to get the mechanisms then we create a
# dictionary for each user having the game names as the keys and the lists of
# mechanisms as the values.
#
# FUNCTIONS:
#
# The main page of each board game can be accessed via
# "https://boardgamegeek.com/boardgame/" + game_id ,
# without mentioning its "web name", ie: "https://boardgamegeek.com/boardgame/135779"
# redirects to
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"

# The list of mechanisms if found on the "credits" page (in javascript code),
# and not the main page.
# The credits page needs the "web name" of the boardgame, eg:
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york/credits"

# We need to get the actual page address since the name of the boardgame and
# the name on the webpage (ie the "web name") can be different:
# eg: "A Fake Artist Goes to New York" and
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"


import pandas as pd
import numpy as np
from collections import Counter
import requests
from selenium import webdriver
import re
import time


def main():
    # In order to use this script on your own files, you must alter:
    # 1. The name tag for the csv file that will be saved as name + '_mechanisms.csv'
    name = "Test"
    # 2. The path to the csv file with the user's collection data:
    datafile = "test_bgg_data.csv"
    dataframe = pd.read_csv(datafile)
    dataframe = data_clean(dataframe=dataframe)
    mechanisms_list = get_all_mechs(dataframe=dataframe)
    mechanisms_series = mechanism_count(mechanisms_list=mechanisms_list)
    save_and_print(series=mechanisms_series, name=name)
    return None


def geturl(game_id: str) -> str:
    """
    Returns the url for bgg main page of game, given id.
    Uses regular expressions.
    :param game_id: string with the number id for game.
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


def data_clean(dataframe):
    df = dataframe.copy()
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
    return df


def get_all_mechs(dataframe) -> list:
    # The following loop grabs the mechanisms of
    # each game in the data frame and appends them to a list.
    mechanisms_list = []
    # length of dataframe to be used in percentage of completion.
    N = dataframe.shape[0]
    # opening the browser
    Firefox = webdriver.Firefox()
    start = time.time()
    j = 1
    for i, row in dataframe.iterrows():
        mechanisms = getmechanisms(row['objectid'], Firefox)
        mechanisms_list += mechanisms
        elapsed_time = time.time() - start
        status_string = '{}\n time elapsed: {:.1f}s\n completed: {:.1f}%'.format(row['objectname'], elapsed_time, (j*100)/N)
        print(status_string)
        j +=1
    print('\n')
    # quit the browser
    Firefox.quit()
    return mechanisms_list


def mechanism_count(mechanisms_list):
    """
    takes the list of mechanisms and returns a pandas series
    with the mechanisms in the index and the number of occurences
    on the column.
    :param mechanisms_list: list of mechanisms
    :return: pandas Series
    """
    # convert the list to a dictionary where each unique
    # entry is a key and the number of times
    # it shows up on the list is the value.
    mechanisms_dict = dict(Counter(mechanisms_list))
    # make a Pandas Series from the dictionary
    Smec = pd.Series(mechanisms_dict)
    return Smec


def save_and_print(series, name):
    """
    Saves the Series to a csv file and prints the
    top 20 entries.
    :param series: Series as in the output of mechanism_count()
    :return: None
    """
    series.to_csv(name + "_mechanisms.csv")
    # print the 20 largest entries
    ranked = series.nlargest(20).reset_index()
    ranked.set_index(ranked.index.map(lambda x: x + 1), inplace=True)
    print('Top 20 most common board game mechanisms in collection.')
    print(name)
    print(ranked)
    return None


if __name__ == '__main__':
    main()
