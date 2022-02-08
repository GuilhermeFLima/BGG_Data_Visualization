import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from selenium import webdriver
import re

# first we need to get the actual page title since the name of the boardgame and
# the name on the webpage can be different:
# eg: "A Fake Artist Goes to New York" and "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"

game_id = "135779"
main_page_url = "https://boardgamegeek.com/boardgame/" + game_id
main_page = requests.get(main_page_url)
main_page_text = main_page.text
#print(main_page_text)
address_pattern = '(https://boardgamegeek.com/boardgame/[\d]+/[\w-]+)'
address_regex = re.compile(address_pattern)
address_find = address_regex.search(main_page_text)
main_address = main_page_text[address_find.start():address_find.end()]
print(main_address)


# pattern = r'(?:href=\"/boardgamemechanic.*?)>([\w /-]+?)<'
# regex = re.compile(pattern)
#
# url = "https://boardgamegeek.com/boardgame/31260/agricola/credits"
# driver = webdriver.Firefox()
# driver.get(url)
# source_text = driver.page_source
# print(regex.findall(source_text))
# driver.quit()
#
# url2 = "https://boardgamegeek.com/boardgame/342942/ark-nova/credits"
# driver = webdriver.Firefox()
# driver.get(url2)
# source_text = driver.page_source
# print(regex.findall(source_text))
# driver.quit()
