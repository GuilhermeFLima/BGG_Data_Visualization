# Here we will grab the current (since mechanisms are updated by users,
# wiki-style) distribution of game mechanisms in bgg
# and save to bggmechanismscount.csv.
# First get the list of mechanisms from bgg, their
# main web pages, and then their count, which will require
# javascript scrapping.

import pandas as pd
import requests
from selenium import webdriver
import re


def main():
    # getting the list of board game mechanisms from bgg
    meclist = getmeclist()
    mecdf = mechanism_counter(meclist)
    mecdf.to_csv("bggmechanismscount.csv")
    return None


def getmeclist():
    url = "https://boardgamegeek.com/browse/boardgamemechanic"
    page = requests.get(url)
    page_text = page.text
    id_pattern = r"/boardgamemechanic/([\d]+)/[\w-]+\"[\s]*>([\w:\s\-,/]+)<"
    id_regex = re.compile(id_pattern)
    id_find = id_regex.findall(page_text)
    return id_find


def findcount(mecid: str, driver) -> int:
    """
    Given the bgg number id of a mechanism, finds the count
    of how of how many board games feature it.
    The webdriver must be opened before and quit after function call.
    :param mecid: the number id
    :param driver: the driver for a selenium browser
    :return: occurences of mechanism
    """

    pattern = r"See All \(([\d,]+)\)"
    regex = re.compile(pattern)
    url = "https://boardgamegeek.com/boardgamemechanic/" + mecid
    # driver = webdriver.Firefox()
    driver.get(url)
    source_text = driver.page_source
    # driver.quit()
    count = regex.findall(source_text)[0]
    count = int(count.replace(',', ''))
    return count


def mechanism_counter(list_of_mechanisms):
    # create dataframe
    mecdf = pd.DataFrame(list_of_mechanisms)
    # rename columns
    mecdf.columns = ['mecid', 'mechanism']
    # open browser
    Firefox = webdriver.Firefox()
    countlist = []
    for i, row in mecdf.iterrows():
        mec_id = row['mecid']
        count = findcount(mec_id, Firefox)
        countlist.append(count)

    # close browser
    Firefox.quit()
    mecdf['count'] = countlist
    return mecdf


if __name__ == '__main__':
    main()



