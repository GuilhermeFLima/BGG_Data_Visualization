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

# Here we will grab the distribution of mechanisms in bgg
# and save to bggmechanismscount.csv.
# First get the list of mechanisms from bgg, their
# main web pages, and then their count, which will require
# javascript scrapping.

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

# getting the list of board game mechanisms from bgg
meclist = getmeclist()
# create dataframe
mecdf = pd.DataFrame(meclist)
# rename columns
mecdf.columns = ['mecid', 'mechanism']
# open browser
Firefox = webdriver.Firefox()

countlist = []
for i, row in mecdf.iterrows():
    id = row['mecid']
    count = findcount(id, Firefox)
    countlist.append(count)

# close browser
Firefox.quit()
mecdf['count'] = countlist
mecdf.to_csv("bggmechanismscount.csv")
